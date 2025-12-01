# Use Node 18
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

# Install Angular CLI globally
RUN npm install -g @angular/cli

# Install dependencies
RUN npm install

# Copy all frontend source code
COPY . .

# Expose Angular dev port
EXPOSE 55909

# Start Angular in Docker
CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "55909"]