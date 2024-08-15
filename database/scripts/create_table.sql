CREATE TABLE IF NOT EXISTS Words(
    WordID INTEGER primary key autoincrement,
    Spelling text,
    Pronunciation text,
    Translate text,
    CardID integer,
    Rang integer,
    TimeRepeat text,
    FOREIGN KEY (CardID) REFERENCES Cards
);

CREATE TABLE IF NOT EXISTS Cards(
    CardID INTEGER primary key autoincrement,
    Name text
);

CREATE TABLE IF NOT EXISTS Sentences(
    SentenceID INTEGER primary key autoincrement,
    Sentence text,
    Translate text,
    ConstructionID INTEGER,
    FOREIGN KEY (ConstructionID) REFERENCES Constructions
);

CREATE TABLE IF NOT EXISTS Constructions(
    ConstructionID INTEGER primary key autoincrement,
    Construction text,
    Translate text
);

CREATE TABLE IF NOT EXISTS Rules(
    RuleID INTEGER primary key autoincrement,
    Rule text,
    Name text
)