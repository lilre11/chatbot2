# Docker Deployment Guide

This guide covers how to deploy the Chatbot2 application using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+
- At least 2GB RAM available
- Ports 80, 443, 1433, 3000, 5000 available

## Quick Start

### Development Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cb2
   ```

2. **Start development environment:**
   ```bash
   # Linux/macOS
   ./deploy.sh build
   
   # Windows
   deploy.bat build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:1433

### Production Deployment

1. **Create production environment file:**
   ```bash
   cp .env.production.template .env.production
   ```

2. **Edit production configuration:**
   ```bash
   nano .env.production  # Update with your actual values
   ```

3. **Deploy to production:**
   ```bash
   # Linux/macOS
   ./deploy.sh deploy
   
   # Windows
   deploy.bat deploy
   ```

4. **Access the application:**
   - Application: http://localhost (via Nginx)
   - Direct Backend: http://localhost:5000
   - Database: localhost:1433

## Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_PASSWORD` | SQL Server SA password | `YourStrong@Passw0rd123!` |
| `SECRET_KEY` | Flask secret key | `your-super-secret-key` |
| `GEMINI_API_KEY` | Google Gemini API key | `your-gemini-api-key` |
| `ADMIN_EMAIL` | Admin user email | `admin@yourdomain.com` |
| `ADMIN_PASSWORD` | Admin user password | `secure-admin-password` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `LOG_LEVEL` | Application log level | `INFO` |
| `BCRYPT_LOG_ROUNDS` | Password hashing rounds | `12` |

## Service Architecture

### Services

1. **Backend (Flask API)**
   - Port: 5000
   - Health check: `/api/health`
   - Resources: 1 CPU, 512MB RAM

2. **Frontend (React SPA)**
   - Port: 3000 (development) / 80 (production)
   - Nginx reverse proxy
   - Resources: 0.5 CPU, 256MB RAM

3. **Database (SQL Server)**
   - Port: 1433
   - Persistent volume: `mssql_data`
   - Resources: 1 CPU, 1GB RAM

4. **Nginx (Production only)**
   - Ports: 80, 443
   - SSL termination
   - Static file serving
   - Resources: 0.5 CPU, 256MB RAM

## Deployment Commands

### Build Commands
```bash
# Build all images
./deploy.sh build

# Build specific service
docker-compose -f docker-compose.prod.yml build backend
```

### Management Commands
```bash
# Start services
./deploy.sh deploy

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# View logs
./deploy.sh logs

# Check health
./deploy.sh health

# Clean up resources
./deploy.sh cleanup
```

### Database Commands
```bash
# Initialize database
docker-compose exec backend python -c "from app import create_app; from services.database_service import DatabaseService; app = create_app(); app.app_context().push(); DatabaseService().init_db()"

# Create admin user
docker-compose exec backend python -c "from app import create_app; from services.database_service import DatabaseService; app = create_app(); app.app_context().push(); DatabaseService().create_user('admin@example.com', 'password')"

# Backup database
docker-compose exec db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$DB_PASSWORD" -Q "BACKUP DATABASE [chatbot_db] TO DISK = N'/var/opt/mssql/data/chatbot_db.bak'"
```

## Monitoring and Logging

### Health Checks
- Backend: `curl http://localhost:5000/api/health`
- Frontend: `curl http://localhost:3000`
- Database: `docker-compose exec db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$DB_PASSWORD" -Q "SELECT 1"`

### Log Locations
- Backend logs: `./logs/`
- Nginx logs: `./logs/nginx/`
- Database logs: Docker container logs

### Monitoring Commands
```bash
# View service status
docker-compose ps

# View resource usage
docker stats

# View logs (real-time)
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
```

## Troubleshooting

### Common Issues

1. **Database connection timeout**
   - Check if SQL Server container is running
   - Verify DB_PASSWORD is correct
   - Check network connectivity

2. **Frontend build fails**
   - Ensure Node.js dependencies are properly installed
   - Check for JavaScript/TypeScript errors

3. **Backend health check fails**
   - Check Flask application logs
   - Verify database connectivity
   - Check Gemini API key configuration

4. **Nginx proxy errors**
   - Check upstream service availability
   - Verify nginx configuration syntax
   - Check SSL certificates if using HTTPS

### Debug Commands
```bash
# Access backend container
docker-compose exec backend bash

# Access database container
docker-compose exec db bash

# View container logs
docker-compose logs backend

# Check network connectivity
docker-compose exec backend ping db
```

## Security Considerations

### Production Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS with valid certificates
- [ ] Configure proper CORS origins
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable Docker security features
- [ ] Regular security updates

### SSL/TLS Configuration

1. **Generate SSL certificates:**
   ```bash
   mkdir ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout ssl/key.pem -out ssl/cert.pem
   ```

2. **Update nginx configuration:**
   - Edit `nginx.conf` to enable SSL
   - Add certificate paths
   - Configure security headers

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker-compose exec db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$DB_PASSWORD" -Q "BACKUP DATABASE [chatbot_db] TO DISK = N'/var/opt/mssql/data/chatbot_db.bak'"

# Copy backup from container
docker cp $(docker-compose ps -q db):/var/opt/mssql/data/chatbot_db.bak ./backups/
```

### Volume Backup
```bash
# Backup database volume
docker run --rm -v cb2_mssql_data:/data -v $(pwd):/backup alpine tar czf /backup/mssql_backup.tar.gz /data
```

### Restore Database
```bash
# Restore from backup
docker-compose exec db /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$DB_PASSWORD" -Q "RESTORE DATABASE [chatbot_db] FROM DISK = N'/var/opt/mssql/data/chatbot_db.bak'"
```

## Performance Optimization

### Resource Limits
- Adjust CPU and memory limits in `docker-compose.prod.yml`
- Monitor resource usage with `docker stats`
- Scale services as needed

### Caching
- Redis cache for session storage
- Nginx static file caching
- Database query optimization

### Load Balancing
- Multiple backend instances
- Database read replicas
- CDN for static assets

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Check GitHub issues
4. Contact the development team
