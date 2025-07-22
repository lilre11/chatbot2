@echo off
setlocal enabledelayedexpansion

REM Production deployment script for Chatbot2
set "COMPOSE_FILE=docker-compose.prod.yml"
set "ENV_FILE=.env.production"

REM Colors (limited in Windows)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"

:log_info
echo %GREEN%[INFO]%NC% %~1
goto :eof

:log_warn
echo %YELLOW%[WARN]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:check_prerequisites
call :log_info "Checking prerequisites..."

REM Check if docker is installed
docker --version >nul 2>&1
if !errorlevel! neq 0 (
    call :log_error "Docker is not installed. Please install Docker first."
    exit /b 1
)

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if !errorlevel! neq 0 (
    call :log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit /b 1
)

REM Check if environment file exists
if not exist "%ENV_FILE%" (
    call :log_warn "Environment file %ENV_FILE% not found. Creating from template..."
    copy .env.example "%ENV_FILE%" >nul
    call :log_warn "Please edit %ENV_FILE% with your production values before running again."
    exit /b 1
)

call :log_info "Prerequisites check passed!"
goto :eof

:build_images
call :log_info "Building Docker images..."
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" build --no-cache
if !errorlevel! neq 0 (
    call :log_error "Failed to build images!"
    exit /b 1
)
call :log_info "Images built successfully!"
goto :eof

:deploy
call :log_info "Deploying application..."

REM Stop existing containers
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" down

REM Start new containers
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" up -d
if !errorlevel! neq 0 (
    call :log_error "Failed to deploy application!"
    exit /b 1
)

call :log_info "Application deployed successfully!"
goto :eof

:check_health
call :log_info "Checking application health..."

REM Wait for services to be ready
timeout /t 10 /nobreak >nul

REM Check backend health
curl -f http://localhost:5000/api/health >nul 2>&1
if !errorlevel! neq 0 (
    call :log_error "Backend health check failed!"
    call :show_logs
    exit /b 1
)
call :log_info "Backend is healthy!"

REM Check frontend
curl -f http://localhost:3000 >nul 2>&1
if !errorlevel! neq 0 (
    call :log_error "Frontend health check failed!"
    call :show_logs
    exit /b 1
)
call :log_info "Frontend is healthy!"

call :log_info "All services are healthy!"
goto :eof

:show_logs
call :log_info "Showing recent logs..."
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" logs --tail=50
goto :eof

:cleanup
call :log_info "Cleaning up old Docker resources..."
docker system prune -f
docker volume prune -f
call :log_info "Cleanup completed!"
goto :eof

:stop
call :log_info "Stopping application..."
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" down
call :log_info "Application stopped!"
goto :eof

:restart
call :log_info "Restarting application..."
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" restart
call :log_info "Application restarted!"
goto :eof

:main
if "%~1"=="build" (
    call :check_prerequisites
    call :build_images
) else if "%~1"=="deploy" (
    call :check_prerequisites
    call :build_images
    call :deploy
    call :check_health
) else if "%~1"=="logs" (
    call :show_logs
) else if "%~1"=="health" (
    call :check_health
) else if "%~1"=="cleanup" (
    call :cleanup
) else if "%~1"=="stop" (
    call :stop
) else if "%~1"=="restart" (
    call :restart
) else (
    echo Usage: %0 {build^|deploy^|logs^|health^|cleanup^|stop^|restart}
    echo.
    echo Commands:
    echo   build    - Build Docker images
    echo   deploy   - Full deployment (build + deploy + health check)
    echo   logs     - Show application logs
    echo   health   - Check application health
    echo   cleanup  - Clean up old Docker resources
    echo   stop     - Stop the application
    echo   restart  - Restart the application
    exit /b 1
)

goto :eof

call :main %*
