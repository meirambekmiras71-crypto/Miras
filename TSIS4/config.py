import pygame

WIDTH  = 600
HEIGHT = 600
CELL   = 30
FPS    = 5

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (180, 180, 180)
DGRAY      = (100, 100, 100)
RED        = (255, 0,   0)
DARK_RED   = (120, 0,   0)
GREEN      = (0,   200, 0)
BLUE       = (0,   0,   255)
YELLOW     = (255, 200, 0)
ORANGE     = (255, 140, 0)
PURPLE     = (150, 0,   200)

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_db",
    "user":     "postgres",
    "password": "12345678"
}