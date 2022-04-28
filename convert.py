import os
import pathlib
import logging
import concurrent.futures
import subprocess


def convert_with_calibre(in_epub, out_epub):
    args = ['/Applications/calibre.app/Contents/MacOS/ebook-convert',
            in_epub, out_epub]
    subprocess.run(args)


if __name__ == '__main__':
    books_path = os.path.join(os.getcwd(), 'Books')
    logger = logging.getLogger()
    output_dir = os.path.join(os.getcwd(), 'converted')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for book_dir in os.listdir(books_path):
        bookdir_path = pathlib.Path(os.path.join(books_path, book_dir))
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as pool:
            if pathlib.Path.is_dir(bookdir_path):
                for item in os.listdir(bookdir_path):
                    os.chdir(bookdir_path)
                    path = pathlib.Path(item)
                    if path.suffix == '.epub':
                        try:
                            out_epub = os.path.join(output_dir, f'{bookdir_path.name}.epub')
                            if os.path.exists(out_epub):
                                raise FileExistsError(f'{bookdir_path.name} already exists. Skipped...')
                            pool.submit(convert_with_calibre, item, out_epub)
                        except Exception as e:
                            logger.warning(e)
