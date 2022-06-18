# Pyrdle

An implementation of Wordle made in [pygame](https://www.pygame.org) for a university project.

Pyrdle includes additional features compared to the original game, such as custom languages or difficulty selection.

![pyrdle-preview-sm](https://user-images.githubusercontent.com/13191399/174433309-13a64ba8-5f6e-4d37-be05-70b13d4f8d74.png)
![pyrdle-sm](https://user-images.githubusercontent.com/13191399/174433290-726d8d8e-1f9d-4e6f-955c-b78501b9e113.gif)

## Prerequisites

- Python 3.10
- dependencies specified in the requirements file

To install dependencies:
```bash
   $> pip install -r .\requirements.txt
```

## Running

Run the main.py file to start the game:
```bash
   $> py -3.10 main.py
```

## Language or theme selection
To change language or theme, call the game constructor in the `main.py` with appropriate parameters, i.e:
```python
wordle = Wordle("polish", Difficulty.MEDIUM, Theme.DARK)
```

You might need to import the enums first. You can also overwrite default values in the constructor.

## Additional languages

**Pyrdle** supports additional languages, including ones with Unicode characters.

### Adding a new language

You can add your own language with only a few steps:
1. Create a directory for the dictionary files in the _resources_ folder, i.e. **french**
2. Add `.csv` files to the **french** directory, where each file contains either 5, 6 or 7 letter words.<br/>
3. Add a new entry in the `config.json` file. Use available entries as a guide.
4. Refer to [Additional languages](#additional-languages) section in order to set another language.

## Authors
[Patryk Wyszyński](https://github.com/patrykwyszyn)<br/>
[Szymon Skórka](https://github.com/sskorka)

## Attributions
Ambience music: The Corner Office by _Blue Dot_ (under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/))
