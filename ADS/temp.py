
print(newimg.getpixel((0,1)))
for index in range(len(converted_secret)):
    if i >= i_width and j >= i_height:
        break
    word = converted_secret[index]
    for k in range(len(word)):
        r,g,b = newimg.getpixel((i, j))
        p = G = g % 9
        q = B = b % 9
        # print(word[k],"=>" ,G,B)
        k = int(k)
        # if (G-1 >= 0 and G+1 < 9) and (B-1 >= 0 and B+1 < 9):
        flag = r % 2
        if(not flag):
            r+=1
        if G-1 >= 0 and random_matrix[G-1][B] == k :
            p = G-1
            q = B
        elif B-1>=0 and random_matrix[G][B-1] == k :
            p = G
            q = B-1
        elif G+1 <9 and random_matrix[G+1][B] == k :
            p = G+1
            q = B
        elif B+1 < 9 and random_matrix[G][B+1] == k :
            p = G
            q = B+1
        elif G-1 >=0 and B-1 >=0 and random_matrix[G-1][B-1] == k :
            p = G-1
            q = B-1
        elif G-1 >=0 and B+1 < 9 and random_matrix[G-1][B+1] == k :
            p = G-1
            q = B+1
        elif G+1 < 9 and B-1 >=0 and random_matrix[G+1][B-1] == k :
            p = G+1
            q = B-1
        elif G+1 < 9 and B+1 < 9 and random_matrix[G+1][B+1] == k :
            p = G+1
            q = B+1
        else:
            r -=1

        if(r % 2 != 0):
            i +=1
            j +=1
            continue
        else:
            g = str(g)[:len(str(g))-1] + str(p)
            b = str(b)[:len(str(b))-1] + str(q)
            newimg.putpixel((i, j), (int(r), int(g), int(b)))
            i+=1
            j+=1
        break
    break


print(newimg.getpixel((0,1)))