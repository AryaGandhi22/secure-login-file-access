const { Client, Account, Databases, Storage, ID, Query, Permission, Role } = Appwrite;

const client = new Client();

client
    .setEndpoint("https://sgp.cloud.appwrite.io/v1")
    .setProject("6a7843d1000988a6defd");

const account = new Account(client);
const databases = new Databases(client);
const storage = new Storage(client);

// Appwrite resources
const DATABASE_ID = "secure-login-db";
const FILES_TABLE_ID = "files";
const BUCKET_ID = "user-files";

async function appwriteRegister() {
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value;

    try {
        const user = await account.create(
            ID.unique(),
            email,
            password
        );

        return {
            status: 201,
            body: {
                message: "User registered successfully",
                userId: user.$id,
                email: user.email
            }
        };
    } catch (error) {
        return {
            status: error.code || 400,
            body: {
                message: error.message
            }
        };
    }
}

async function appwriteLogin() {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
        const session = await account.createEmailPasswordSession(
            email,
            password
        );

        return {
            status: 200,
            body: {
                message: "Login successful",
                sessionId: session.$id
            }
        };
    } catch (error) {
        return {
            status: error.code || 401,
            body: {
                message: error.message
            }
        };
    }
}
async function appwriteLogout() {
    try {
        await account.deleteSession("current");

        return {
            status: 200,
            body: {
                message: "Logout successful"
            }
        };
    } catch (error) {
        return {
            status: error.code || 400,
            body: {
                message: error.message
            }
        };
    }
}
async function appwriteMe() {
    try {
        const user = await account.get();

        return {
            status: 200,
            body: {
                id: user.$id,
                email: user.email,
                name: user.name
            }
        };
    } catch (error) {
        return {
            status: error.code || 401,
            body: {
                message: error.message
            }
        };
    }
}
async function appwriteGetFiles() {
    try {
        const user = await account.get();

        const result = await databases.listDocuments(
            DATABASE_ID,
            FILES_TABLE_ID,
            [
                Query.equal("ownerID", user.$id)
            ]
        );

        return {
            status: 200,
            body: result.documents
        };

    } catch (error) {
        return {
            status: error.code || 401,
            body: {
                message: error.message
            }
        };
    }
}
async function appwriteGetFileById(id) {
    try {
        const user = await account.get();

        const file = await databases.getDocument(
            DATABASE_ID,
            FILES_TABLE_ID,
            id
        );

        if (file.ownerID !== user.$id) {
            return {
                status: 403,
                body: {
                    message: "You do not have access to this file"
                }
            };
        }

        return {
            status: 200,
            body: file
        };

    } catch (error) {
        return {
            status: error.code || 404,
            body: {
                message: error.message
            }
        };
    }
}
async function appwriteDownloadFile(id) {
    try {
        const user = await account.get();

        // Get metadata first
        const file = await databases.getDocument(
            DATABASE_ID,
            FILES_TABLE_ID,
            id
        );

        // Verify ownership
        if (file.ownerID !== user.$id) {
            return {
                status: 403,
                body: {
                    message: "You do not have access to this file"
                }
            };
        }

        // Get the actual Storage file
        const result = storage.getFileDownload(
            BUCKET_ID,
            file.fileId
        );

        return {
            status: 200,
            url: result.toString(),
            filename: file.filename
        };

    } catch (error) {
        return {
            status: error.code || 404,
            body: {
                message: error.message
            }
        };
    }
}