# Deployment Guide

## FastAPI Backend with Kogic Docker Sandbox

This guide covers deploying the modular FastAPI backend system with Vite frontend and Kogic sandbox container.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ (for local development)
- Node.js 18+ (for frontend development)
- Ubuntu 22.04 (recommended for Kogic sandbox)

## Quick Start

### 1. Clone and Setup

\`\`\`bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-kogic-system

# Create environment file
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 2. Environment Configuration

Create `.env` file with:

\`\`\`env
# Application
ENVIRONMENT=development
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=postgresql://kogic_user:kogic_password@postgres:5432/kogic_db

# AI Services
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key

# Frontend
VITE_API_URL=http://localhost:8000
VITE_ENVIRONMENT=development
\`\`\`

### 3. Docker Deployment

\`\`\`bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
\`\`\`

### 4. Access Services

- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Vite Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Development Setup

### Backend Development

\`\`\`bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

# Run development server
cd scripts/fastapi_backend
python main.py
\`\`\`

### Frontend Development

\`\`\`bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

## Production Deployment

### 1. Production Docker Compose

Create `docker-compose.prod.yml`:

\`\`\`yaml
version: '3.8'

services:
  fastapi-backend:
    build:
      context: .
      target: base
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - fastapi-backend
\`\`\`

### 2. Nginx Configuration

\`\`\`nginx
upstream fastapi_backend {
    server fastapi-backend:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
\`\`\`

## Kogic Sandbox Configuration

### Security Settings

\`\`\`bash
# Create sandbox user
docker exec -it kogic-sandbox useradd -m sandbox
docker exec -it kogic-sandbox usermod -aG docker sandbox

# Set resource limits
docker update --memory=1g --cpus=1 kogic-sandbox
\`\`\`

### Allowed Commands

Edit `docker-compose.yml` to configure allowed commands:

\`\`\`yaml
kogic-sandbox:
  environment:
    - ALLOWED_COMMANDS=python3,node,npm,curl,wget,git
    - MAX_EXECUTION_TIME=300
    - MAX_MEMORY=1G
\`\`\`

## Monitoring and Logging

### Health Checks

\`\`\`bash
# Check backend health
curl http://localhost:8000/health

# Check all services
docker-compose ps
\`\`\`

### Log Management

\`\`\`bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f fastapi-backend

# Export logs
docker-compose logs > system.log
\`\`\`

## Scaling

### Horizontal Scaling

\`\`\`yaml
# Scale backend instances
docker-compose up -d --scale fastapi-backend=3

# Load balancer configuration
nginx:
  depends_on:
    - fastapi-backend
  deploy:
    replicas: 1
\`\`\`

### Database Scaling

\`\`\`yaml
# PostgreSQL with read replicas
postgres-primary:
  image: postgres:15-alpine
  environment:
    - POSTGRES_REPLICATION_MODE=master

postgres-replica:
  image: postgres:15-alpine
  environment:
    - POSTGRES_REPLICATION_MODE=slave
    - POSTGRES_MASTER_SERVICE=postgres-primary
\`\`\`

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Permission errors**: Check file ownership and Docker permissions
3. **Memory issues**: Increase Docker memory limits
4. **Database connection**: Verify DATABASE_URL and network connectivity

### Debug Commands

\`\`\`bash
# Enter container shell
docker exec -it kogic-fastapi-backend bash

# Check container resources
docker stats

# View container configuration
docker inspect kogic-fastapi-backend
\`\`\`

## Security Considerations

1. **Change default secrets** in production
2. **Use HTTPS** with proper SSL certificates
3. **Implement rate limiting** for API endpoints
4. **Regular security updates** for base images
5. **Network isolation** between services
6. **Backup strategies** for data persistence

## Backup and Recovery

\`\`\`bash
# Database backup
docker exec kogic-postgres pg_dump -U kogic_user kogic_db > backup.sql

# Volume backup
docker run --rm -v kogic_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore database
docker exec -i kogic-postgres psql -U kogic_user kogic_db < backup.sql
