from enum import Enum

class UserTypeEnum(Enum):
    ADMIN = 1
    EDITOR = 2
    VIEWER = 3

    @staticmethod
    def reverse_mapping():
        return {
            1: "Admin User",
            2: "Editor User",
            3: "Viewer"
        }        

class CategoryEnum(Enum):
    PAINTINGS = 1
    PHOTOGRAPHY = 2
    DRAWINGS = 3
    SCULPTURE = 4
    COLLAGE = 5
    PRINTMAKING = 6
    DIGITAL = 7

    @staticmethod
    def reverse_mapping(): 
        return {
            1: "Paintings",
            2: "Photography",
            3: "Drawings",
            4: "Sculpture",
            5: "Collage",
            6: "Printmaking",
            7: "Digital"
        }
    
class StyleEnum(Enum):
    DIGITAL_ART = 1
    ABSTRACT = 2
    MODERN = 3
    FINE_ART = 4
    POP_ART = 5
    GEOMATRIC = 6
    
    @staticmethod
    def reverse_mapping():
        return {
            1: "Digital Art",
            2: "Abstract",
            3: "Modern",
            4: "Fine Art",
            5: "Pop Art",
            6: "Geomatric"
        }

class MaterialEnum(Enum):
    CANVAS = 1
    WOOD = 2
    PAPER = 3
    COLOR = 4
    ACRYLIC = 5
    GLASS = 6
    OIL = 7
    FINE_ART_PAPER = 8

    @staticmethod
    def reverse_mapping():
        return {
            1: "Canvas",
            2: "Wood",
            3: "Paper",
            4: "Color",
            5: "Acrylic",
            6: "Glass",
            7: "Oil",
            8: "Fine Art Paper",
        }

class MediumEnum(Enum):
    ACRYLIC = 1
    OIL = 2
    WATERCOLOR = 3
    PAPER = 4
    COLOR = 5
    PAINT = 6
    PENCIL = 7
    DIGITAL = 8
    METAL = 9
    WOOD = 10
    
    @staticmethod
    def reverse_mapping():
        return {
            1: "Acrylic",
            2: "Oil",
            3: "Watercolor",
            4: "Paper",
            5: "Color",
            6: "Paint",
            7: "Pencil",
            8: "Digital",
            9: "Metal",
            10: "Wood"
        }

class SubjectEnum(Enum):
    ABSTRACT = 1
    PEOPLE = 2
    PORTRAIT = 3
    ANIMAL = 4
    NATURE = 5
    BEACH = 6
    GEOMATRIC = 7
    
    @staticmethod
    def reverse_mapping():
        return {
            1: "Abstract",
            2: "People",
            3: "Portrait",
            4: "Animal",
            5: "Nature",
            6: "Beach",
            7: "Geomatric"
        }

class OrientationEnum(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    SQUARE = 3
    
    @staticmethod
    def reverse_mapping():
        return {
            1: "Horizontal",
            2: "Vertical",
            3: "Square",
        }
