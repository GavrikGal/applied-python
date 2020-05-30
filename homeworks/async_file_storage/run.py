import filestorage
import sys
import logging

logging.basicConfig(level=logging.ERROR)

if len(sys.argv) < 2:
    logging.error('Требуется запуск с указанием конфиругационного файла')
else:
    config_path = sys.argv[1]
    file_storage = filestorage.FileStorage(config_path)
    file_storage.run()
