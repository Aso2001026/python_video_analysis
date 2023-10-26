import cv2

cap = cv2.VideoCapture('./video/bad.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
count = 0
image_No = 0
save_path = './image/bad/'

#read first bg frame
bg = None

while cap.isOpened():

    #read video frame
    ret, frame = cap.read()
    if ret == False: 
        print('no video')
        break

    #resize video frame
    frame = cv2.resize(frame, (1280, 720))

    #フレームに座標を書き込む
    cv2.putText(frame, str(count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    #remove noise
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    #gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #read first bg frame
    if bg is None:
        bg = gray.copy()
        continue

    #diff frame
    diff = cv2.absdiff(gray, bg)
        
    #threshold
    _, diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
    # diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, kernel)



    #find contours
    contours, _ = cv2.findContours(diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #draw contours
    for contour in contours:
        area = cv2.contourArea(contour)


        if area >5 and area < 100:
            x, y, w, h = cv2.boundingRect(contour)
            if  x < 150 or x > 1070 or w > 50 or h > 50: break # ノイズを除去
            # 抽出した領域を画像として保存
            imgex = frame[y:y+h, x:x+w]
            # outfile =  save_path + "/" + str(image_No) + ".jpg"
            # cv2.imwrite(outfile, imgex)
            # image_No += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
           

            

    #update bg
    bg = gray.copy()


    #show video    
    cv2.imshow('bad', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('diff', diff)
    if cv2.waitKey(1) == 13: 
        break
    
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)