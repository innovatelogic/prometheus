import * as vscode from 'vscode';
import * as path from 'path';

import { io, Socket } from "socket.io-client";
const socket: Socket = io('http://127.0.0.1:8088');


import { FileNode } from './FileNode';

export function activate(context: vscode.ExtensionContext) {
    // Register the command to show the file hierarchy
    const disposable = vscode.commands.registerCommand('helloworld.showFileHierarchy', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder is open.');
            return;
        }

        socket.on('connect', () => console.log('Connected'));
        //const ws = new WebSocket('ws://127.0.0.1:8088/socket.io/');

        //ws.addEventListener('open', () => {
        //    vscode.window.showInformationMessage('WebSocket connected to 127.0.0.1:8080');
        //});

        // Start parsing files from the root of the workspace
        const rootFolder = workspaceFolders[0].uri.fsPath;
        const hierarchy = await buildFileHierarchy(rootFolder);

        // Create and show a Webview Panel
        const panel = vscode.window.createWebviewPanel(
            'fileHierarchy', // Internal ID
            'File Hierarchy', // Title of the panel
            vscode.ViewColumn.One, // Show in the first column
            {
                enableScripts: true // Allow JavaScript in the Webview
            }
        );

        // Generate and set the HTML content for the Webview
        panel.webview.html = getWebviewContent(hierarchy);
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}

// Recursively build the file hierarchy
async function buildFileHierarchy(folderPath: string): Promise<FileNode> {
    const rootNode = new FileNode(folderPath, path.basename(folderPath));

    const children = await vscode.workspace.fs.readDirectory(vscode.Uri.file(folderPath));
    for (const [childName, childType] of children) {
        const childPath = path.join(folderPath, childName);

        if (childType === vscode.FileType.Directory) {
            // Recursively parse subdirectories
            const childNode = await buildFileHierarchy(childPath);
            rootNode.children.push(childNode);
        } else if (childType === vscode.FileType.File) {
            // Parse files and look for includes
            const fileNode = new FileNode(childPath, childName);
            await parseIncludes(childPath, fileNode);
            rootNode.children.push(fileNode);
        }
    }

    return rootNode;
}

// Parse #include statements in a file
async function parseIncludes(filePath: string, fileNode: FileNode): Promise<void> {
    const fileContent = await vscode.workspace.fs.readFile(vscode.Uri.file(filePath));
    const contentString = fileContent.toString();

    // Extract #include statements
    const includeRegex = /#include\s+["<](.*?)[">]/g;
    let match;
    while ((match = includeRegex.exec(contentString)) !== null) {
        const includePath = match[1];
        fileNode.children.push(new FileNode(includePath, includePath));
    }
}

// Generate HTML content for the Webview
function getWebviewContent(hierarchy: FileNode): string {
    const hierarchyHtml = generateHierarchyHtml(hierarchy);

    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Hierarchy</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 10px; }
                ul { list-style-type: none; padding-left: 20px; }
                li { margin: 5px 0; }
            </style>
        </head>
        <body>
            <h1>File Hierarchy</h1>
            <ul>
                ${hierarchyHtml}
            </ul>
        </body>
        </html>
    `;
}

// Recursively generate HTML for the file hierarchy
function generateHierarchyHtml(node: FileNode): string {
    if (node.children.length === 0) {
        return `<li>${node.name}</li>`;
    }

    const childrenHtml = node.children.map(child => generateHierarchyHtml(child)).join('');
    return `<li>${node.name}<ul>${childrenHtml}</ul></li>`;
}

