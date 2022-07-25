# News search engine


https://user-images.githubusercontent.com/59199865/180759013-8cf4e1c6-ccc8-459f-9b39-b2e0610aaa87.mov

## How to start
1. install vue/cli for front project
```
npm install -g @vue/cli
```
2. install python >= 3.8 with following [guide](https://www.python.org/downloads/) for back project
3. clone the project with following command
```
git clone git@github.com:IR1401-Spring-Final-Projects/News1401-13.git
```
4. install requirments with following command
```
pip install -r requirements.txt
```
5. some models are not on git due to maximum file size so for running project download them from links given and locate them in given path</br>
* path: data/news.json | link: [link](https://drive.google.com/file/d/1IJ-TIaBDC9FuRDsQSETQu4F0PhRKO4n9/view?usp=sharing)</br>
* path: models/classification_logistic_regression_improved/fasttext/fasttext.bin | link: [link](https://drive.google.com/file/d/1K3zfBdJw1YjStBYAdOGdeH-J_iY9LfxP/view?usp=sharing) </br>
* path: models/classification_transformers/pytorch_model.bin | link: [link](https://drive.google.com/file/d/14Tsv-xD9Gzn2OOjRnTYb8KlyqMEw46MC/view?usp=sharing)</br>
* path: models/clustering/fasttext/fasttext.bin | link: [link](https://drive.google.com/file/d/1K3zfBdJw1YjStBYAdOGdeH-J_iY9LfxP/view?usp=sharing)</br>
* path: models/fasttext_search/fasttext.bin | link: [link](https://drive.google.com/file/d/1K3zfBdJw1YjStBYAdOGdeH-J_iY9LfxP/view?usp=sharing)</br>
* path: models/preprocessed_data/data.plk | link: [link](https://drive.google.com/file/d/1lSepeGQDCoZvYtKTTnvtDGmYRpRPqn4F/view?usp=sharing)</br>
* path: models/preprocessed_data/clf_data.plk | link: [link](https://drive.google.com/file/d/1MJ9fqdsN6Yg7pNTwOCvgIXjTgVrCB7AI/view?usp=sharing)</br>
* path: models/QE_fasttext/fasttext.bin | link: [link](https://drive.google.com/file/d/1K3zfBdJw1YjStBYAdOGdeH-J_iY9LfxP/view?usp=sharing)</br>
* path: models/QE_fasttext/all_words_vectors_emb_fasttext.json | link: [link](https://drive.google.com/file/d/1pfOCdNSMnrMB8kRnQMkqjKrFNiVcBARA/view?usp=sharing)</br>
* path: models/transformers_search/transformer_model.model/pytorch_model.bin | link: [link](https://drive.google.com/file/d/1gUCUBA6dCy5MfuxLHoVynBq52HSUI0Dw/view?usp=sharing)</br>
* path: models/transformers_search/transformer_vectors_emb.json | link: [link](https://drive.google.com/file/d/1agsbUbWVD06RhypXXOevxzSTljKjlHqJ/view?usp=sharing)</br>
6. run backend project with following command
```
uvicorn src.api:app --reload 
```
7. go to `front/search_engine` and run frontend project with following command
```
npm run serve
```
enjoy it!</br></br>
