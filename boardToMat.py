import cv2
import numpy as np
import os

def load_piece_images(image_dir='piece_images'):
    pieces = {}
    for piece_name in os.listdir(image_dir):
        piece_dir = os.path.join(image_dir, piece_name)
        pieces[piece_name] = []
        for img_file in os.listdir(piece_dir):
            img_path = os.path.join(piece_dir, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            pieces[piece_name].append(img)
    return pieces

def match_piece(square_image, pieces):
    square_gray = cv2.cvtColor(square_image, cv2.COLOR_BGR2GRAY)
    max_val = -1
    best_match = None
    
    for piece_name, templates in pieces.items():
        for template in templates:
            template_resized = cv2.resize(template, (square_gray.shape[1], square_gray.shape[0]))
            result = cv2.matchTemplate(square_gray, template_resized, cv2.TM_CCOEFF_NORMED)
            min_val, match_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if match_val > max_val:
                max_val = match_val
                best_match = piece_name
                
    if max_val > 0.5:  # Adjust threshold as needed
        return best_match
    return '00'  # Empty square

def reorder_points(pts):
    pts = pts.reshape((4, 2))
    new_pts = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    new_pts[0] = pts[np.argmin(s)]
    new_pts[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    new_pts[1] = pts[np.argmin(diff)]
    new_pts[3] = pts[np.argmax(diff)]

    return new_pts

def extract_chessboard(image_path, pieces):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    chessboard_contour = contours[0]

    epsilon = 0.1 * cv2.arcLength(chessboard_contour, True)
    approx_corners = cv2.approxPolyDP(chessboard_contour, epsilon, True)

    if len(approx_corners) != 4:
        raise ValueError("Could not find a proper chessboard contour.")

    corners = reorder_points(approx_corners)
    width, height = 800, 800
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(corners, dst)
    warped = cv2.warpPerspective(image, M, (width, height))

    # Display the warped chessboard
    cv2.imshow('Warped Chessboard', warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Initialize the chessboard matrix
    chess_matrix = [['00' for _ in range(8)] for _ in range(8)]
    square_size = width // 8

    for i in range(8):
        for j in range(8):
            # Extract each square
            square = warped[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size]

            # Display each square (for debugging purposes)
            #cv2.imshow(f'Square ({i},{j})', square)
            #cv2.waitKey(100)

            # Detect the piece on the square
            piece = match_piece(square, pieces)
            chess_matrix[i][j] = piece

    cv2.destroyAllWindows()

    return chess_matrix

def main():
    pieces = load_piece_images(image_dir='chess_pieces')
    board_matrix = extract_chessboard('image.png', pieces)
    return board_matrix

if __name__ == "__main__":
    main()
