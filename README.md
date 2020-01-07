# Novel Generation

This repository contains a simple language model that can be used to generate random text resembling a source document. It is written from scratch and does not use any external libraries such as Numpy or NLTK.

Here is the explanation for the [8-queen](https://en.wikipedia.org/wiki/Eight_queens_puzzle) variant

This was made as an exercise to implement a ngram model and understand Markov models on NLP. So please take in account that this code was written in a few days without any professional review/standard .

## Getting Started

The file ["ngram_model.py"](ngram_model.py) contains all the code and our ngram model to generate text from a text file source.

The [frankenstein.txt](frankenstein.txt) file contains the whole novel of the same name so you can try out the ngram model on it to generate similar text.

## Running the model

The following function call will create a ngram model of size "n" from a given text:

```[python]
model = create_ngram_model(n, path_to_text_file)
```

You can then generate text from the model using the following function call:

```[python]
model.random_text(token_count)
```

"token_count" denotes the amount of tokens (words) you want to generate from the model.

You can also calculate the perplexity of a sentence using the following function call:

```[python]
model.perplexity(some_setence_as_string)
```

## Authors

- **Raphael Van Hoffelen** - [github](https://github.com/dskart) - [website](https://www.raphaelvanhoffelen.com/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
