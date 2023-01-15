# NTFS

## NTFS Basic permissions

| Permission Type | Description |
| --- | --- |
| Full Control | reading, writing, changing, deleting of files/folders |
| Modify | reading, writing, deleting of files/folders |
| List Folder Contents | viewing, listing folders and subfolders, executing files. Folders only inherit this permission |
| Read and Execute | viewing, listing files and subfolders, executing files. Files and folders inherit this permissions |
| Write | adding files to folders and subfolders, writing to a file |
| Read | viewing, listing folders and subfolders, viewing a files's contents |
| Traverse Folder | allows or denies the ability to move through folders to reach other files or folders |

## NTFS Special permissions

| Permission | Description |
| --- | --- |
| Full Control | Users are permitted or denied permissions to add, edit, move, delete files and folders as well as change NTFS permissions that apply to all permitted folders |
| Traverse folder / execute file | Users are permitted or denied permissions to access a subfolder within a directory structure even if the user is denied access to contents at the parent folder level. users may also be permitted or denied permissions to execute programs |
| List folder/read data | users are permitted or denied permissions to view files and folders contained in the parent folder. users can also be permitted to open and view files |
| Read attributes | Users are permitted or denied permissions to view basic attributes of a file or folder. Examples of basic attributes: system, archive, read-only, and hidden |
| Read extended attributes | Users are permitted or denied permissions to view extended attributes of a file or folder. Attributes differ depending on the program |
| Create files/write data | Users are permitted or denied permissions to create files within a folder and make changes to a file |
| Create folders/append data | Users are permitted or denied permissions to create subfoldes within a folder. Data can be added to files but pre-existing content cannot be overwritten |
| Write attributes | Users are permitted or denied to change file attributes. This permissions does not grant access to creating files or folders |
| Write extended attributes | Users are permitted or denied permissions to change extended attributes on a file or folder. Attributes differ depending on the program |
| Delete subfolders and files | Users are permitted or denied permissions to delete subfolders and files. Parent folders will not be deleted |
| Delete | Users are permitted or denied permissions to delete parent folders, subfolders and files |
| Read permissions | Users are permitted or denied permissions to read permissions of a folder |
| Change permissions | Users are permitted or denied permissions to change permissions of a file or folder |
| Take ownership | Users are permitted or denied permission to take ownership of a file or folder. The owner of a file has full permissions to change any permissions |
