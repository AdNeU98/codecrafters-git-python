import sys
import os
import zlib

def printContentOfFile(totalContent):
    if b'\x00' in totalContent:
        header, contentOfFile = totalContent.split(b'\x00')
        decodedContent = contentOfFile.decode('utf-8')
        print(decodedContent.strip(), end='') 

def main():
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    if command == "cat-file":
        if sys.argv[2] == "-p" and len(sys.argv[3]) == 40 :
            blob_sha = sys.argv[3]
            blob_folder = blob_sha[:2]
            blob_hash = blob_sha[2:]
            path = ".git/objects/" + blob_folder + "/" + blob_hash
            with open(path, 'rb') as f:
                totalContent = zlib.decompress(f.read())
                printContentOfFile(totalContent)       
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
