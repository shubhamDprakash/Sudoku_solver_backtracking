import cv2
import numpy as np

bo_initial = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

bo = [x[:] for x in bo_initial]

def valid(num, row, column):
    #check row validity
    for i in range(9):
        if num == bo[row][i] and i != column:
            return False
    
    #check column validity
    for i in range(9):
        if num == bo[i][column] and i != row :
            return False
    
    #check box validity
    row_interval = row//3
    column_interval = column//3
    for i in range(row_interval*3, (row_interval+1)*3):
        for j in range(column_interval*3, (column_interval+1)*3):
            if bo[i][j] == num and (i,j) != (row, column):
                    return False
    return True


def print_board(bo):
    print('  ~ ~ ~   ~ ~ ~   ~ ~ ~  ')
    for i in range(9):
        print('|', end=" ")
        for j in range(9):
            if j%3 == 2:
                print(f'{bo[i][j]} |', end=" ")
            else:
                print(bo[i][j], end=" ")
        print()
        if i%3 == 2:
            print('  ~ ~ ~   ~ ~ ~   ~ ~ ~  ')


def show_board(bo):
    width, height = 630, 630
    image = np.ones((height, width, 3)) * 255
    box_height = height//9
    box_width = width//9

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    textsize = cv2.getTextSize(str(bo[0][0]), font, font_scale, font_thickness)[0]
    no_width, no_height = textsize
    
    for i in range(0, height + box_height, box_height):
        if i % 3 == 0:
            cv2.line(image, (0, i), (width, i), (0,0,0), thickness=font_thickness)
        cv2.line(image, (0, i), (width, i), (0,0,0), thickness=1)

    for i in range(0, width + box_width, box_width):
        if i % 3 == 0:
            cv2.line(image, (i, 0), (i, height), (0,0,0), thickness=font_thickness)
        cv2.line(image, (i, 0), (i, height), (0,0,0), thickness=1)
    
    for i in range(9):
        for j in range(9):
            if bo_initial[i][j] != 0:
                cv2.putText(image, str(bo_initial[i][j]), (j*box_width + (box_width - no_width)//2, i*box_height+box_height-(box_height-no_height)//2), font, font_scale, (0,0,0), font_thickness, cv2.LINE_AA)
            elif bo_initial[i][j] == 0 and bo[i][j] != bo_initial[i][j]:
                cv2.putText(image, str(bo[i][j]), (j*box_width + (box_width - no_width)//2, i*box_height+box_height-(box_height-no_height)//2), font, font_scale, (0,255,0), font_thickness, cv2.LINE_AA)

    cv2.imshow('board', image)
    return


def solve():
    global bo
    show_board(bo)
    cv2.waitKey(100)
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                for k in range(1,10):
                    if valid(k, i, j):
                        bo[i][j] = k
                        solve()
                        bo[i][j] = 0
                return
    print_board(bo)
    input("More?")


solve()
cv2.destroyAllWindows()
