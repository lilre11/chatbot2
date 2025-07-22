#!/bin/bash

# Production deployment script for Chatbot2
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if environment file exists
    if [[ ! -f "$ENV_FILE" ]]; then
        log_warn "Environment file $ENV_FILE not found. Creating from template..."
        cp .env.example "$ENV_FILE"
        log_warn "Please edit $ENV_FILE with your production values before running again."
        exit 1
    fi
    
    log_info "Prerequisites check passed!"
}

build_images() {
    log_info "Building Docker images..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache
    log_info "Images built successfully!"
}

deploy() {
    log_info "Deploying application..."
    
    # Stop existing containers
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down
    
    # Start new containers
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
    
    log_info "Application deployed successfully!"
}

check_health() {
    log_info "Checking application health..."
    
    # Wait for services to be ready
    sleep 10
    
    # Check backend health
    if curl -f http://localhost:5000/api/health &>/dev/null; then
        log_info "Backend is healthy!"
    else
        log_error "Backend health check failed!"
        show_logs
        exit 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 &>/dev/null; then
        log_info "Frontend is healthy!"
    else
        log_error "Frontend health check failed!"
        show_logs
        exit 1
    fi
    
    log_info "All services are healthy!"
}

show_logs() {
    log_info "Showing recent logs..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs --tail=50
}

cleanup() {
    log_info "Cleaning up old Docker resources..."
    docker system prune -f
    docker volume prune -f
    log_info "Cleanup completed!"
}

# Main script
case "${1:-deploy}" in
    "build")
        check_prerequisites
        build_images
        ;;
    "deploy")
        check_prerequisites
        build_images
        deploy
        check_health
        ;;
    "logs")
        show_logs
        ;;
    "health")
        check_health
        ;;
    "cleanup")
        cleanup
        ;;
    "stop")
        log_info "Stopping application..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down
        log_info "Application stopped!"
        ;;
    "restart")
        log_info "Restarting application..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" restart
        log_info "Application restarted!"
        ;;
    *)
        echo "Usage: $0 {build|deploy|logs|health|cleanup|stop|restart}"
        echo ""
        echo "Commands:"
        echo "  build    - Build Docker images"
        echo "  deploy   - Full deployment (build + deploy + health check)"
        echo "  logs     - Show application logs"
        echo "  health   - Check application health"
        echo "  cleanup  - Clean up old Docker resources"
        echo "  stop     - Stop the application"
        echo "  restart  - Restart the application"
        exit 1
        ;;
esac
