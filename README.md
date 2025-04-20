# Vocabulary Card

This is a project of my own to review words I had looked up in the translation application [pot-app](https://github.com/pot-app/pot-desktop).

## Usage

1. Make a copy of `config.yaml.json` and rename it to `config.yaml`.
2. Edit `config.yaml` to change `db_name` item to your `history.db` path which should be a path like `C:\\Users\\<your_user_name>\\AppData\\Roaming\\com.pot-app.desktop\\history.db`.

## Develop

```shell
npm i
npm run dev
```

## Build

```shell
npm i
npm run build # or npm run build:unpack
```

The executable file and installer is in `dist` folder.

## Todos

- [ ] Theme
- [ ] Dictation