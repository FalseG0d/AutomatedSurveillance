import cv2
import datetime
import time

from Modules.object_detection import check_frame

def Processing(file, file_save):
    if file == '0':
        file = int(file)
        
    cap = cv2.VideoCapture(file)

    ret,frame1 = cap.read()
    ret,frame2 = cap.read()
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    Output = cv2.VideoWriter(file_save, fourcc, 20.0, (640, 352))

    count=0

    start_time=time.time()

    while cap.isOpened():
        diff = cv2.absdiff(frame1,frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(9,9),0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations = 3)
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        datex = str(datetime.datetime.now())
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame1,datex,(10,20),font,0.5,(255,255,255),1,cv2.LINE_AA)


        if contours == None :

            cv2.putText(frame1, "STATUS : STATIONARY", (480,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

        else :
            count=count+1
            for contour in contours :
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 1500 :
    #                 cv2.putText(frame1, "STATUS : STATIONARY", (480,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
                    continue
                cv2.rectangle(frame1, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(frame1, "STATUS : MOVEMENT", (480,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

                if time.time()-start_time>3:
                    # cv2.imshow("Frame%d.jpg"%count,frame1)

                    ### OBJECT DETECTION
                    
                    objects=check_frame(frame2)
                    print(objects)

                    ### OBJECT DETECTION

                    start_time=time.time()
                
#                cv2.drawContours(frame1, contours, -1, (255,255,0), 2)
        # cv2.imshow('FEED', diff)
        # cv2.imshow('FEED', gray)
        # cv2.imshow('FEED', blur)
        # cv2.imshow('FEED', thresh)
        # cv2.imshow('FEED', dilated)
        
        cv2.imshow('FEED', frame1)      #Video Feed
        
        B = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        L = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        Output.write(frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27 :
            break

    cv2.destroyAllWindows()
    
File = "VideoInput/Cam_Detection.mp4" #input('\nEnter location of video: ')
File_Save = "Output/Cam_Detection.avi" #input('\nEnter the location to save video: ')

Processing(File, File_Save)

File