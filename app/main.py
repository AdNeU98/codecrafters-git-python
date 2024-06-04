import sys
import os
import zlib
import hashlib

def printContentOfFile(totalContent):
    if b'\x00' in totalContent:
        header, contentOfFile = totalContent.split(b'\x00')
        decodedContent = contentOfFile.decode('utf-8')
        print(decodedContent.strip(), end='') 

def create_blob(path:str):
    with open(path, "rb") as f:
        data = f.read()
    header = f"blob {len(data)}\0".encode("utf-8")
    store = header + data
    sha = hashlib.sha1(store).hexdigest()
    os.makedirs(f".git/objects/{sha[:2]}", exist_ok=True)
    with open(f".git/objects/{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(store))
    return sha

def commit(tree_sha, parent_sha, message):
    content = f"tree {tree_sha}\nparent {parent_sha}\nAnirban Dutta <dutta.an@northeastern.edu>\ncommiter Anirban Dutta <dutta.an@northeastern.edu>\n\n{message}\n"
    data = f"commit {len(content)}\0{content}".encode()
    sha = hashlib.sha1(data).hexdigest()
    os.makedirs(f".git/objects/{sha[:2]}", exist_ok=True)
    with open(f".git/objects/{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(data))
    return sha


def write_tree(path:str):
    if os.path.isfile(path):
        return create_blob(path)    
    contents = sorted(os.listdir(path),
        key=lambda x: x if os.path.isfile(os.path.join(path, x)) else f"{x}/",
    )
    eachEncodedContent = b""
    for each in contents:
        if each == ".git":
            continue
        eachContentPath = os.path.join(path, each)
        if os.path.isfile(eachContentPath):
            eachEncodedContent += f"100644 {each}\0".encode()
        else: 
            eachEncodedContent += f"40000 {each}\0".encode()
        eachItemsha = int.to_bytes(int(write_tree(eachContentPath), base=16), length=20, byteorder="big")
        eachEncodedContent += eachItemsha

    eachEncodedContent = f"tree {len(eachEncodedContent)}\0".encode() + eachEncodedContent
    eachItemsha = hashlib.sha1(eachEncodedContent).hexdigest()
    os.makedirs(f".git/objects/{eachItemsha[:2]}", exist_ok=True)
    with open(f".git/objects/{eachItemsha[:2]}/{eachItemsha[2:]}", "wb") as f:
        f.write(zlib.compress(eachEncodedContent))
    return eachItemsha
            
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
    elif command == "cat-file":
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
    elif command == "hash-object":
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
    elif command == "ls-tree": #TEST with `python3 app/main.py ls-tree --name-only <tree_sha>`
        if sys.argv[2] == "--name-only" and len(sys.argv[3]) == 40:
            tree_sha = sys.argv[3]
            tree_folder = tree_sha[:2]
            tree_hash = tree_sha[2:]
            path = ".git/objects/" + tree_folder + "/" + tree_hash
            with open(path, 'rb') as f:
                totalContent = zlib.decompress(f.read())
                _, binary_data = totalContent.split(b"\x00", maxsplit=1)
                while binary_data:
                    mode, dataLeftOver = binary_data.split(b"\x00", maxsplit=1)
                    modeNumber, modeType = mode.split()
                    binary_data = dataLeftOver[20:]
                    print(modeType.decode('utf-8'))
    elif command == "write-tree":
        print(write_tree("./"))
    elif command == "commit-tree":
        tree_sha = sys.argv[2]
        parent_sha = sys.argv[4]
        message = sys.argv[6]
        sha = commit(tree_sha, parent_sha, message)
        print(sha)

    else:
        raise RuntimeError(f"Unknown command #{command}")
        
if __name__ == "__main__":
    main()
