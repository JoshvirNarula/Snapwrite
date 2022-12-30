#average time
#average accuracy
#average low confidence words


import os
import time
import statistics as stat


def detect_document(path):
    global avgtime
    global avgaccuracy_block
    global avgaccuracy_word
    global avgaccuracy_symbol
    global avg_low_symbol
    global avg_low_word
    global block_count
    global lowsymbols
    global t_word_count
    global t_symbol_count

    start = time.time()
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    end = time.time()

    low_word_count=0
    low_symbol_count=0
    word_count=0
    symbol_count=0

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            avgaccuracy_block+=block.confidence
            block_count+=1
            
            
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_count+=1
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    avgaccuracy_word+=word.confidence   
                    if(word.confidence<=0.90):
                        low_word_count+=1
                

                    for symbol in word.symbols:
                        symbol_count+=1
                        avgaccuracy_symbol+=symbol.confidence
                        if(symbol.confidence<=0.90):
                            low_symbol_count+=1
                            lowsymbols.append(symbol.text)
                    

    avg_low_word+=low_word_count/word_count
    avg_low_symbol+=low_symbol_count/symbol_count
    t_word_count+=word_count
    t_symbol_count+=symbol_count

    avgtime+=(end-start)


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



avgtime=0.0
avgaccuracy_block=0.0
avgaccuracy_word=0.0
avgaccuracy_symbol=0.0
avg_low_word=0
avg_low_symbol=0
lowsymbols=[]
block_count=0
file_count=0
t_word_count=0
t_symbol_count=0


directory='/Users/joshvirnarula/snapwrite/testing_dataset/snapwrite_testdataset/Sentence Testing'


for filename in os.listdir(directory):
    file_name = os.path.join(directory, filename)
    file_count+=1
    detect_document(file_name)
    print("processed" , file_count , "images..")
    
print()
print("number of images processed:" , file_count)
print("Total time taken by vision:" , avgtime)
print("Average time taken by vision:" , (avgtime/file_count))
print()
print("Average accuracy of blocks:" , (avgaccuracy_block/block_count))
print("Average accuracy of words:" , (avgaccuracy_word/t_word_count))
print("Average accuracy of symbols:" , (avgaccuracy_symbol/t_symbol_count))
print()
print("Average percentage of low accuracy words per image:" , (avg_low_word/file_count))
print("Average percentage of low accuracy symbols per image:" , (avg_low_symbol/file_count))
print("Most common low accuracy symbol:" , stat.mode(lowsymbols))






