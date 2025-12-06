import stdlib.__entry__ as stdlib
import os

cinitCode = """
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#if defined(_WIN32)
    #include <direct.h>
    #define MKDIR(path) _mkdir(path)
    #define GETCWD _getcwd
#else
    #include <unistd.h>
    #include <sys/types.h>
    #include <sys/stat.h>

    #define GETCWD getcwd
    #define MKDIR(path) mkdir(path, 0755)
#endif

#if defined(_WIN32)
    #define PATH_SEP '\\'
#else
    #define PATH_SEP '/'
#endif

char* path_join(const char* p1, const char* p2) {
    size_t len1 = strlen(p1);
    size_t add_sep = (len1 > 0 && p1[len1 - 1] != PATH_SEP) ? 1 : 0;

    char* result = malloc(len1 + add_sep + strlen(p2) + 1);
    if (!result) return NULL;

    strcpy(result, p1);

    if (add_sep)
        result[len1] = PATH_SEP, result[len1 + 1] = '\\0';

    strcat(result, p2);
    return result;
}


int write_bytes_to_file(const char *path, const unsigned char *data, size_t size) {
    FILE *f = fopen(path, "wb");
    if (!f) {
        perror("fopen");
        return 0;
    }

    size_t written = fwrite(data, 1, size, f);
    fclose(f);

    return written == size;
}


"""

def string_to_hex_list(s: str, include_null=False):
    data = s.encode("utf-8")
    result = [f"0x{b:02X}" for b in data]

    if include_null:
        result.append("0x00")

    return result

def walker(start):
    indexy = 0
    indexy2 = 0
    full = "char buffer[2024];\nif (GETCWD(buffer, sizeof(buffer)) == NULL) {\nperror(\"getcwd error\"); return 1;\n}\n"
    for dp, dn, fn in os.walk(start):
        for d in dn:
            full += f"char* directory_{indexy} = path_join(buffer, \"{os.path.relpath(os.path.join(dp, d).replace("\\", "/"), start).replace("\\", "/")}\");\nMKDIR(directory_{indexy});\nprintf(\"Directory: %s\\n\", directory_{indexy});\nfree(directory_{indexy});\n"
            indexy += 1
        for f in fn:
            pathy = os.path.join(dp, f)
            rel = os.path.relpath(pathy, start)
            by = stdlib.filesystem()
            byte = by.readFromFile(pathy).decode("utf-8", errors="replace") # returns bytes
            listy = stdlib.clear_empty_gap(string_to_hex_list(byte))
            full += f"char* file_{indexy2} = path_join(buffer, \"{rel.replace("\\", "/")}\");\n"
            full += f"unsigned char bytes_{indexy2}[] = " + "{ " + ", ".join(listy) + " };" + "\n"
            full += f"write_bytes_to_file(file_{indexy2}, bytes_{indexy2}, sizeof(bytes_{indexy2}));\nprintf(\"File: %s\\n\", file_{indexy2});\n"
            full += f"free(file_{indexy2});\n"
            indexy2 += 1
    return full

def packager(start):
    full = cinitCode
    full += "int main() {"
    full += walker(start)
    full += "return 0;\n}"
    return full

