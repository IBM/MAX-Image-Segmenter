import os
import shutil


def copy_dir(source_directory,
             target_directory):
    """
        Copies files from source_directory to\
         target_directory. If target directory doesn't exist\
         it will be created.
        :param source_directory: source
        :type source_directory: str

        :param adict: if specified, adict will be printed
        :type adict: dict
    """
    if os.path.isdir(source_directory):
        def deep_copy(source, target):
            """Copies recursively all files from source to destination
            """
            names = os.listdir(source)
            os.makedirs(target, exist_ok=True)
            for name in names:
                src_name = os.path.join(source, name)
                tgt_name = os.path.join(target, name)
                if os.path.isdir(src_name):
                    # source is a directory
                    deep_copy(src_name, tgt_name)
                else:
                    # source is a file
                    print('Copying "{}" to "{}" ...'
                          .format(src_name, tgt_name))
                    shutil.copy2(src_name, tgt_name)

        # copy files recursively
        deep_copy(source_directory,
                  target_directory)
    else:
        print('Error. Directory "{}" was not found.'.format(source_directory))
