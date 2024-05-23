import sys
import os
import zlib
import hashlib

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
        return
    if command == "cat-file":
        if sys.argv[2] == "-p" and len(sys.argv[3]) == 40 :
            blob_sha = sys.argv[3]
            blob_folder = blob_sha[:2]
            blob_hash = blob_sha[2:]
            path = ".git/objects/" + blob_folder + "/" + blob_hash
            try:
                with open(path, 'rb') as f:
                    totalContent = zlib.decompress(f.read())
                    printContentOfFile(totalContent)
                    return
            except zlib.error as e:
                 print(f"Error occurred during decompression: {e}")
            except IOError as e:
                print(f"File error: {e}")
    if command == "hash-object":
        if sys.argv[2] == "-w" and len(sys.argv[3]) != 0:
            file_name = sys.argv[3]
            with open(file_name, 'rb') as f:
                contentOfFile = f.read()
                contentSHA = b"blob" + b" " + str(len(contentOfFile)).encode('utf-8') + b"\0" + contentOfFile
                sha1_hash = hashlib.sha1()
                sha1_hash.update(contentSHA)
                hash_output = sha1_hash.hexdigest()
                os.mkdir(".git/objects/" + hash_output[:2])
                sha_file_name = os.path.join(".git/objects/", hash_output[:2], hash_output[2:])
                with open(sha_file_name, 'wb')  as f:
                    f.write(zlib.compress(contentSHA))
                    print(hash_output, end='')
                    return
    else:
        raise RuntimeError(f"Unknown command #{command}")
        
if __name__ == "__main__":
    main()
