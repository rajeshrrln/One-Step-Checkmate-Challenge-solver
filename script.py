class ChessBoard:
    def __init__(self,board) -> None:
        self.board = board
    def is_valid(self,pos):
        i,j = pos
        return 0<=i<8 and 0<=j<8
    def is_same_color(self,pos1,pos2):
        i,j = pos1
        x,y = pos2
        return self.board[i][j][0].lower() == self.board[x][y][0].lower() != '0'
    def is_empty(self,pos):
        return self.board[pos[0]][pos[1]] == '00'
    def is_white(self,pos):
        if self.is_empty(pos):
            return False
        return self.board[pos[0]][pos[1]][0].lower() == 'w'
    def is_black(self,pos):
        if self.is_empty(pos):
            return False
        return self.board[pos[0]][pos[1]][0].lower() == 'b'
    def slide(self,i,j,pos):
        lst = []
        x,y = pos
        x+=i
        y+=j
        while self.is_valid((x,y)):
            if self.is_empty((x,y)):
                lst.append((x,y))
            elif not self.is_same_color(pos,(x,y)):
                lst.append((x,y))
                break
            else:
                break
            x+=i
            y+=j
        return lst
    def all_possible_moves(self,pos):
        places = []
        i = pos[0]
        j = pos[1]
        piece = self.board[i][j][1].lower()
        color = self.board[i][j][0].lower()
        #PAWN
        if piece == 'p':
            if color == 'b':
                if self.is_empty((i-1,j)) and self.is_valid((i-1,j)):
                    places.append((i-1,j))
                if self.is_valid((i-2,j)) and i == 6 and self.is_empty((i-2,j)):
                    places.append((i-2,j))
                if self.is_valid((i-1,j+1)) and not self.is_same_color(pos,(i-1,j+1)) and not self.is_empty((i-1,j+1)):
                    places.append((i-1,j+1))
                if  self.is_valid((i-1,j-1)) and not self.is_same_color(pos,(i-1,j-1)) and not self.is_empty((i-1,j-1)):
                    places.append((i-1,j-1))
                return places
            else:
                if self.is_empty((i+1,j)) and self.is_valid((i+1,j)):
                    places.append((i+1,j))
                if self.is_valid((i+2,j)) and i == 1 and self.is_empty((i+2,j)):
                    places.append((i+2,j))
                if self.is_valid((i+1,j+1)) and not self.is_same_color(pos,(i+1,j+1)) and not self.is_empty((i+1,j+1)):
                    places.append((i+1,j+1))
                if  self.is_valid((i+1,j-1)) and not self.is_same_color(pos,(i+1,j-1))and not self.is_empty((i+1,j-1)):
                    places.append((i+1,j-1))
                return places

        #ROOK
        if piece == 'r':
            places.extend(self.slide(-1,0,pos))
            places.extend(self.slide(1,0,pos))
            places.extend(self.slide(0,-1,pos))
            places.extend(self.slide(0,1,pos))
            return places
        #KNIGHT
        if piece == 'n':
            possible = [(i-2,j-1),(i-2,j+1),(i+2,j-1),(i+2,j+1),(i+1,j-2),(i+1,j+2),(i-1,j+2),(i-1,j-2)]
            for posi in possible:
                if self.is_valid(posi) and not self.is_same_color(pos,posi):
                    places.append(posi)
            return places
        #BISHOP
        if piece == 'b':
            places.extend(self.slide(1,1,pos))
            places.extend(self.slide(-1,-1,pos))
            places.extend(self.slide(1,-1,pos))
            places.extend(self.slide(-1,1,pos))
            return places
        #QUEEN
        if piece == 'q':
            #Rook code
            places.extend(self.slide(-1,0,pos))
            places.extend(self.slide(1,0,pos))
            places.extend(self.slide(0,-1,pos))
            places.extend(self.slide(0,1,pos))
            #Bishop code
            places.extend(self.slide(1,1,pos))
            places.extend(self.slide(-1,-1,pos))
            places.extend(self.slide(1,-1,pos))
            places.extend(self.slide(-1,1,pos))
            return places
            
        #KING
        if piece == 'k':
            possible = [(i+1,j),(i+1,j+1),(i+1,j-1),(i,j-1),(i,j+1),(i-1,j-1),(i-1,j),(i-1,j+1)]
            for posi in possible:
                if self.is_valid(posi) and not self.is_same_color(pos,posi):
                    places.append(posi)
            return places
    def is_white_checked(self):
        all_dangered_places=set()
        wk_pos = None
        for i in range(8):
            for j in range(8):
                if self.board[i][j].lower() == 'wk':
                    wk_pos = (i,j)
                if self.is_black((i,j)):
                    all_dangered_places.update(set(self.all_possible_moves((i,j))))
        if wk_pos in all_dangered_places:
            return True
        return False
    def is_checkmate(self):
        if not self.is_white_checked():
            return False
        for i in range(8):
            for j in range(8):
                if self.is_white((i,j)):
                    possible_moves = self.all_possible_moves((i,j))
                    for x,y in possible_moves:
                        removed = self.board[x][y]
                        self.board[x][y] = self.board[i][j]
                        self.board[i][j] = '00'
                        ans = self.is_white_checked()
                        self.board[i][j] = self.board[x][y]
                        self.board[x][y] = removed
                        if not ans:
                            return False
        return True
    def solve(self):
        for i in range(8):
            for j in range(8):
                if self.is_black((i,j)):
                    piece = self.board[i][j][1].lower()
                    possible_moves = self.all_possible_moves((i,j))
                    for x,y in possible_moves:
                        promoted = False
                        freq = 1
                        if piece == 'p' and x==0:
                            freq = 2
                            promoted = True
                        for k in range(freq):
                            removed = self.board[x][y]
                            if promoted and k == 0:
                                self.board[i][j] = 'bq'
                            if promoted and k == 1:
                                self.board[i][j] = 'bn'
                            self.board[x][y] = self.board[i][j]
                            self.board[i][j] = '00'
                            ans = self.is_checkmate() 
                            # Uncomment the below section to display what the board looks like after the move
                            '''
                            if ans:
                                for row in self.board:
                                    print(*row)
                                print()
                            '''
                            self.board[i][j] = self.board[x][y]
                            self.board[x][y] = removed
                            if promoted:
                                self.board[i][j] = 'bp'
                            if ans is True:
                                return [(i,j),(x,y)]
        return None
    # To name the row columns according to the chess conventions
    def findMove(self):
        sent = self.solve()
        if sent == None:
            return "No checkmate found in ONE step !!!!"
        row = {7:8,6:7,5:6,4:5,3:4,2:3,1:2,0:1}
        col = {7:'a',6:'b',5:'c',4:'d',3:'e',2:'f',1:'g',0:'h'}
        piece = {'p':'Pawn','b':'Bishop','q':"Queen",'k':'King','n':'Knight','r':'Rook'}
        src,dest = sent
        i,j = src
        x,y = dest
        ans = f"Move {col[j]}{row[i]} TO {col[y]}{row[x]}"
        return ans



## Example driver code
        
board = [
    ['00', '00', '00', '00', '00', '00', '00', '00'],
    ['00', 'bp', '00', '00', '00', '00', '00', '00'],
    ['wk', '00', '00', '00', '00', '00', '00', '00'],
    ['00', '00', '00', 'bb', '00', '00', '00', '00'],
    ['bk', '00', '00', 'bb', '00', '00', '00', '00'],
    ['00', '00', '00', '00', '00', '00', '00', '00'],
    ['00', '00', '00', '00', '00', '00', '00', '00'],
    ['00', '00', '00', '00', '00', '00', '00', '00']
]

obj = ChessBoard(board)
ans = obj.findMove()
print(ans)

