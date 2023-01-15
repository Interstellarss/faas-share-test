MODEL_DIR := "/models/3dunet"
TENSORFLOW_MODEL := $(MODEL_DIR)/3dunet_kits19_128x128x128.tf
TENSORFLOW_ZIPFILE := 3dunet_kits19_128x128x128.tf.zip
TENSORFLOW_ZIP := $(MODEL_DIR)/$(TENSORFLOW_ZIPFILE)
ZENODO_TENSORFLOW := https://zenodo.org/record/5597155/files/3dunet_kits19_128x128x128.tf.zip?download=1

default: download_tensorflow_model

.PHONY: create_directories
create_directories:
	@echo "Preparing directories..."
	@if [ ! -e $(MODEL_DIR) ]; then \
		mkdir -p $(MODEL_DIR) ; \
	fi

.PHONY: download_tensorflow_model
download_tensorflow_model: create_directories
	@echo "Downloading TensorFlow model from Zenodo..."
	@if [ ! -e $(TENSORFLOW_MODEL) ]; then \
		wget -O $(TENSORFLOW_ZIP) $(ZENODO_TENSORFLOW) \
		&& cd $(MODEL_DIR) && unzip $(TENSORFLOW_ZIPFILE) && rm $(TENSORFLOW_ZIPFILE) && cd -; \
	fi
