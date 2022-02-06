import pygame as pg

class ImageContainer:
  
    @classmethod
    def get_container(self) -> dict:
        tree =  pg.image.load("../images/tree.png").convert_alpha()
        rock =  pg.image.load("../images/rock.png").convert_alpha()
        building01 =  pg.image.load("../images/building01.png").convert_alpha()
        building02 =  pg.image.load("../images/building02.png").convert_alpha()

        return {"tree": tree, 
                "rock": rock,
                "building01":building01,
                "building02":building02}

def cart_to_iso(cartX, cartY):
    isoX = cartX - cartY
    isoY = (cartX + cartY) / 2
    return isoX, isoY

def iso_to_cart(isoX, isoY):
    cart_y = (2 * isoY - isoX) / 2
    cart_x = cart_y + isoX
    return cart_x, cart_y

def draw_text(screen, text, size, color, pos):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color).convert_alpha()
    text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)

def scale_image(image, width=None, height=None):
    if height == None and width != None:
        # makes the h scale the same with width to get desired height
        scale = width / image.get_width()
        height = scale * image.get_height()
        image = pg.transform.scale(image, (int(width), int(height)))
    elif width == None and height != None:
        scale = height / image.get_height()
        width = scale * image.get_width()
        image = pg.transform.scale(image, (int(width), int(height)))
    else:
        image = pg.transform.scale(image, (int(width), int(height)))
    return image
