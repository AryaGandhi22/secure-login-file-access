# Appwrite Implementation

This directory documents the Appwrite implementation of the Secure Login &
File Access System.

The frontend integration is implemented in:

../frontend/appwrite-adapter.js

## Technologies

- Appwrite Authentication
- Appwrite Sessions
- Appwrite Database
- Appwrite Storage
- Appwrite Permissions

## What Appwrite Handles

Appwrite handles:

- User registration
- User authentication
- Session management
- Current-user information
- Session deletion during logout
- Database infrastructure
- File storage
- File access permissions

## What Was Configured

The following Appwrite resources were configured for the application:

- Appwrite project
- Database
- Files collection
- Storage bucket
- Database attributes
- Database permissions
- Storage permissions
- User-to-file relationships

## User and File Relationship

Each uploaded file is associated with the authenticated Appwrite user.

The database stores the file metadata and user relationship, while the actual
document is stored in Appwrite Storage.

User-specific permissions prevent one user from accessing another user's files.

## Demo Users

For testing, create three demo users in the Appwrite project:

| Email | Password |
|---|---|
| alice@example.com | Password123! |
| bob@example.com | Password123! |
| carol@example.com | Password123! |

Create one test file for each user and configure the appropriate permissions.

## Security

Appwrite API keys, server secrets, passwords, and other sensitive credentials
must not be committed to the repository.