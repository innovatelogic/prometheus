// FileNode class to represent files and directories
export class FileNode {
    public children: FileNode[] = [];

    constructor(public readonly path: string, public readonly name: string) {}
}