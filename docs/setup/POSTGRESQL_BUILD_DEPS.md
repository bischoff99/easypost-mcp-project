# PostgreSQL Build Dependencies

## Issue

When installing PostgreSQL via `mise`, the build fails with:
```
configure: error: bison not found
```

## Solution

Install build dependencies before running `mise install`:

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  bison \
  flex \
  libreadline-dev \
  zlib1g-dev \
  libicu-dev \
  libssl-dev \
  uuid-dev
```

### Linux (RHEL/CentOS/Fedora)

```bash
sudo yum install -y \
  gcc \
  gcc-c++ \
  make \
  bison \
  flex \
  readline-devel \
  zlib-devel \
  icu \
  openssl-devel \
  libuuid-devel
```

### macOS

```bash
brew install bison flex readline icu4c openssl
```

## After Installing Dependencies

```bash
# Retry mise install
mise install
```

## Alternative: Use System PostgreSQL

If building PostgreSQL fails, you can use system PostgreSQL instead:

```bash
# Install PostgreSQL via package manager
# Linux (Ubuntu/Debian):
sudo apt-get install postgresql-17

# Linux (RHEL/CentOS):
sudo yum install postgresql17-server

# macOS:
brew install postgresql@17

# Then update DATABASE_URL in .env to use system PostgreSQL
```

## Docker Alternative

For development, consider using Docker instead:

```bash
docker-compose up -d postgres
```

This avoids build dependencies entirely.
