#!/bin/bash
#set -x
COLORS=120
IMAGE="image.png"

if [ ! -z "$1" ]; then
    IMAGE="$1"
fi
if [ ! -z "$2" ]; then
    COLORS="$2"
fi

# Check if the file is an image
MIME_TYPE=$(file --mime-type -b "$IMAGE")
if [[ $MIME_TYPE != image/* ]]; then
    echo "Error: $IMAGE is not an image file."
    exit 1
fi

# Extract file extension
EXT="${IMAGE##*.}"

# Convert to PNG if not PNG already
if [ "$EXT" != "png" ]; then
    echo "Converting $IMAGE to PNG format"
    CONVERTED_IMAGE="${IMAGE%.*}.png"
    convert "$IMAGE" "$CONVERTED_IMAGE"
    IMAGE="$CONVERTED_IMAGE"
fi

echo "Reducing $IMAGE to $COLORS colors"
pngquant "$COLORS" "$IMAGE" --quality 0-100 --verbose -f -s 1 -o "${IMAGE%.*}_reduced.png"

# run your python scripts
python3 palette.py "${IMAGE%.*}_reduced.png"
python3 vertical6_web.py "${IMAGE%.*}_reduced.png" 35 10 40 212

FILE_FILE=$(basename "$IMAGE")
FILE_PATH=$(dirname "$IMAGE")/

echo "$FILE_FILE"
echo "$FILE_PATH"

# use the SAME downloads folder ur flask app uses
ZIP_PATH="/mnt/c/Users/Lavav/Documents/SwiftPrinterWebApp-main/SwiftPrinterWebApp-main/downloads/${FILE_FILE}.zip"

echo "zipping files to $ZIP_PATH"
/usr/bin/zip -j -r "$ZIP_PATH" "${FILE_PATH}image_data.txt" "${FILE_PATH}image_hex.txt" "${IMAGE%.*}_reduced.png"

# optionally cleanup temp files here
# rm "${FILE_PATH}"*png "${FILE_PATH}image_data.txt" "${FILE_PATH}image_hex.txt"
