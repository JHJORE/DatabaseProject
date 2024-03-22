CREATE TABLE IF NOT EXISTS CustomerProfile(
    CID INTEGER PRIMARY KEY AUTOINCREMENT,
    MobileNO INTEGER UNIQUE,
    "Name" TEXT,
    "Address" TEXT
);
CREATE TABLE IF NOT EXISTS CustomerOrder(
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Time" TIME,
    "Date" DATE,
    CID INTEGER NOT NULL,
    CONSTRAINT fk_CID FOREIGN KEY (CID) REFERENCES CustomerProfile(CID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Ticket(
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    PerformanceID INTEGER,
    SegmentID INTEGER,
    OrderID INTEGER NOT NULL,
    ChairNO INTEGER,
    RowNO INTEGER,
    AreaID INTEGER,
    "Name" TEXT,
    THID INTEGER,
    CONSTRAINT fk_OrderID FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT fk_performanceID FOREIGN KEY (PerformanceID) REFERENCES Performance(PerformanceID) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT fk_segmentID FOREIGN KEY (SegmentID) REFERENCES CustomerGroup(SegmentID) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT fk_THID FOREIGN KEY (THID) REFERENCES TheaterHalls(THID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS CustomerGroup(
    SegmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    Segment TEXT
);
CREATE TABLE IF NOT EXISTS Performance(
    PerformanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Date" DATE,
    "Time" TIME,
    PlayID INTEGER,
    CONSTRAINT fk_PlayID FOREIGN KEY (PlayID) REFERENCES TheaterPlay(PlayID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS HasGroup(
    SegmentID INTEGER NOT NULL,
    PlayID INTEGER NOT NULL,
    price INTEGER,
    CONSTRAINT pk_SegmentID_PlayID PRIMARY KEY (SegmentID, PlayID),
    CONSTRAINT fk_SegmentID FOREIGN KEY (SegmentID) REFERENCES CustomerGroup(SegmentID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_PlayID FOREIGN KEY (PlayID) REFERENCES TheaterPlay(PlayID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS TheaterPlay(
    PlayID INTEGER PRIMARY KEY AUTOINCREMENT,
    season TEXT,
    "Name" TEXT,
    THID INTEGER,
    EID INTEGER,
    CONSTRAINT fk_THID FOREIGN KEY (THID) REFERENCES TheaterHalls(THID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Manager(EID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS AssignedBackstage(
    EID INTEGER NOT NULL,
    PlayID INTEGER NOT NULL,
    task TEXT,
    CONSTRAINT pk_EID_PlayID PRIMARY KEY (EID, PlayID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Manager(EID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_PlayID FOREIGN KEY (PlayID) REFERENCES TheaterPlay(PlayID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Employees(
    EID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    "Email" TEXT,
    "Phone" INTEGER,
    "status" TEXT
);
CREATE TABLE IF NOT EXISTS AssignedRole(
    EID INTEGER NOT NULL,
    RoleID INTEGER NOT NULL,
    CONSTRAINT pk_EID_RoleID PRIMARY KEY (EID, RoleID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Employees(EID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_RoleID FOREIGN KEY (RoleID) REFERENCES Role(RoleID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Actor(
    EID INTEGER NOT NULL,
    CONSTRAINT pk_EID PRIMARY KEY (EID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Employees(EID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Manager(
    EID INTEGER NOT NULL,
    CONSTRAINT pk_EID PRIMARY KEY (EID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Employees(EID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS ManagerOf(
    EID INTEGER NOT NULL,
    PlayID INTEGER NOT NULL,
    CONSTRAINT pk_EID_PlayID PRIMARY KEY (EID, PlayID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Manager(EID) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT fk_PlayID FOREIGN KEY (PlayID) REFERENCES TheaterPlay(PlayID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Backstage(
    EID INTEGER NOT NULL,
    CONSTRAINT pk_EID PRIMARY KEY (EID),
    CONSTRAINT fk_EID FOREIGN KEY (EID) REFERENCES Employees(EID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS "Role"(
    RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT
);
CREATE TABLE IF NOT EXISTS RoleInAct(
    RoleID INTEGER NOT NULL,
    NumID INTEGER NOT NULL,
    CONSTRAINT pk_RoleID_NumID PRIMARY KEY (RoleID, NumID),
    CONSTRAINT fk_RoleID FOREIGN KEY (RoleID) REFERENCES "Role"(RoleID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_NumID FOREIGN KEY (NumID) REFERENCES Acts(NumID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Acts(
    NumID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT
);
CREATE TABLE IF NOT EXISTS PartOf(
    NumID INTEGER NOT NULL,
    PlayID INTEGER NOT NULL,
    CONSTRAINT pk_NumID_PlayID PRIMARY KEY (NumID, PlayID),
    CONSTRAINT fk_NumID FOREIGN KEY (NumID) REFERENCES Acts(NumID) ON UPDATE CASCADE ON DELETE NO ACTION CONSTRAINT fk_PlayID FOREIGN KEY (PlayID) REFERENCES TheaterPlay(PlayID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS TheaterHalls(
    THID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" TEXT,
    capacity INTEGER
);
CREATE TABLE IF NOT EXISTS Area(
    THID INTEGER NOT NULL,
    "Name" TEXT NOT NULL,
    CONSTRAINT pk_THID_Name PRIMARY KEY (THID, "Name"),
    CONSTRAINT fk_THID FOREIGN KEY (THID) REFERENCES TheaterHalls(THID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS AreaTheaterHall(
    THID INTEGER NOT NULL,
    "Name" TEXT NOT NULL,
    AreaID INTEGER NOT NULL,
    CONSTRAINT pk_THID_Name_AreaID PRIMARY KEY (THID, "Name", AreaID),
    CONSTRAINT fk_THID_Name FOREIGN KEY (THID, "Name") REFERENCES Area(THID, "Name") ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS ChairInArea(
    THID INTEGER NOT NULL,
    "Name" TEXT NOT NULL,
    AreaID INTEGER NOT NULL,
    ChairNO INTEGER NOT NULL,
    RowNO INTEGER NOT NULL,
    CONSTRAINT pk_THID_Name_AreaID_ChairNO_RowNO PRIMARY KEY (THID, "Name", AreaID, ChairNO, RowNO),
    CONSTRAINT fk_THID_Name_AreaID FOREIGN KEY (THID, "Name", AreaID) REFERENCES AreaTheaterHall(THID, "Name", AreaID) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS Chair(
    THID INTEGER NOT NULL,
    "Name" INTEGER NOT NULL,
    ChairNO INTEGER NOT NULL,
    RowNO INTEGER NOT NULL,
    CONSTRAINT pk_THID_AreaID_ChairNO_RowNO PRIMARY KEY (THID, "Name", ChairNO, RowNO),
    CONSTRAINT fk_THID_AreaID FOREIGN KEY (THID, "Name") REFERENCES Area(THID, "Name") ON UPDATE CASCADE ON DELETE NO ACTION
);