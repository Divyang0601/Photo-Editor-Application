import streamlit as st
import cv2
from PIL import Image,ImageEnhance
import numpy as np
import os
import base58
import imutils
from io import BytesIO

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

angle1 = 90
angle2 = 270
angle3 = 180

def get_image_download_link(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base58.b64encode(buffered.getvalue()).decode()
    href = f'<a href = "data:file/jpg;base58,{img_str}">Download result (Use image extension while downloading)</a>'
    return href


def main():

    st.set_option('deprecation.showfileUploaderEncoding', False)

    activities = ["Foto Filter","Feature Detection","Panorama Generator","Document Scanner","About"]
    option = st.sidebar.selectbox("Select mode :",activities)
    #wide = st.sidebar.slider("Size",100,1000)
    height = st.sidebar.slider("Height :",200,1000,key = 1)
    width = st.sidebar.slider("Width :",200,1000,key = 2)
    amount = ["Select Option","Clockwise 90","Anticlockwise 90","Clockwise 180"]
    rotate = st.sidebar.selectbox("Rotate :",amount)


    if option == "Foto Filter":
        st.title("Foto Editor")
        st.write(""" ## Upload Image ## """)
        image_file = st.file_uploader("To try the filters upload an Image",type = ['jpg','png','jpeg'])

        activity = ["Original","Manual filters","Sketch","Smoothen","B & W","GrayScale","Blurring","Edges"]
        choices = st.sidebar.radio("Try our automated filters : ",activity)

        if image_file is not None:
            my_image = Image.open(image_file)

            if rotate == "Selection Option":
                pass
            elif rotate == "Clockwise 90":
                my_image = my_image.rotate(angle1)
            elif rotate == "Anticlockwise 90":
                my_image = my_image.rotate(angle2)
            elif rotate == "Clockwise 180":
                my_image = my_image.rotate(angle3)
            if choices == 'Original':
                st.text("Original Image")
                my_image = np.array(my_image.convert('RGB'))
                my_image = cv2.resize(my_image,(width,height))
                st.image(my_image)
                my_image = Image.fromarray(my_image)
                st.markdown(get_image_download_link(my_image), unsafe_allow_html = True)

            elif choices == 'Manual filters':

                new_image = my_image

                brightness = st.sidebar.slider("Brightness",1,5)
                enhancer = ImageEnhance.Brightness(new_image)
                new_image = enhancer.enhance(brightness)

                Contrast = st.sidebar.slider("Contrast",1,5)
                enhancer = ImageEnhance.Contrast(new_image)
                new_image = enhancer.enhance(Contrast)

                Sharpness = st.sidebar.slider("Sharpness",1,15)
                enhancer = ImageEnhance.Sharpness(new_image)
                new_image = enhancer.enhance(Sharpness)

                Color = st.sidebar.slider("Color Balance",1,50)
                enhancer = ImageEnhance.Color(new_image)
                new_image = enhancer.enhance(Color)

                Enhance = st.sidebar.slider("Enhance",0,10)
                new_image = ImageEnhance._Enhance()
                new_image = enhancer.enhance(Enhance)

                st.text("Manual filters")
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                st.image(new_image)
                new_image = Image.fromarray(new_image)
                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)



            elif choices == "B & W":
                new_image = np.array(my_image.convert('RGB'))
                new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
                _,th1 = cv2.threshold(new_image,127,255,cv2.THRESH_BINARY)
                st.text("B & W")
                th1 = cv2.resize(th1,(width,height))
                st.image(th1)
                result = Image.fromarray(th1)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

            elif choices == "Sketch":
                new_image =np.array(my_image.convert('RGB'))
                new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
                th2 = cv2.adaptiveThreshold(new_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,3)
                st.text("Sketch")
                th2 = cv2.resize(th2,(width,height))
                st.image(th2)
                result = Image.fromarray(th2)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

            elif choices == "Smoothen":
                new_image = np.array(my_image.convert('RGB'))
                kernel = np.ones((5,5),np.float32)/25
                smooth = cv2.filter2D(new_image,-1,kernel)
                st.text("Smoothened Image")
                smooth = cv2.resize(smooth,(width,height))
                st.image(smooth)
                result = Image.fromarray(smooth)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

            elif choices == 'GrayScale':
                new_image = np.array(my_image.convert('RGB'))
                new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
                st.text("Gray-scale Image")
                new_image = cv2.resize(new_image,(width,height))
                st.image(new_image)
                result = Image.fromarray(new_image)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

            elif choices == 'Blurring':
                new_image = np.array(my_image.convert('RGB'))
                new_image = cv2.GaussianBlur(new_image,(7,7),0)
                st.text("Gaussian Blur")
                new_image = cv2.resize(new_image,(width,height))
                st.image(new_image)
                result = Image.fromarray(new_image)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

            elif choices == 'Edges':
                new_image = np.array(my_image.convert('RGB'))
                new_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
                new_image = cv2.Canny(new_image,100,100)
                st.text("Edge Detect")
                new_image = cv2.resize(new_image,(width,height))
                st.image(new_image)
                result = Image.fromarray(new_image)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

    elif option == "About":
        st.title("Photo Editing Application")
        st.subheader("Built using OpenCV and Streamlit")
        st.write(''' *** Designed by Divyang Mishra***''')
        st.write(''' *** Linkedin : *** https://www.linkedin.com/in/divyang-mishra-67a7651a0/''')
        st.write(''' *** Github : *** https://github.com/Divyang0601''')

    elif option == "Panorama Generator":
        st.title("Create a Panorama using multiple images")
        st.subheader("Image Stitching")

        options = ["2","3"]
        total = st.sidebar.selectbox("Number of images to be upload",options)

        if total == "2":
            image_file1 = st.file_uploader("Upload Image 1",type = ['jpg','png','jpeg'],key = 1)
            image_file2 = st.file_uploader("Upload Image 2",type = ['jpg','png','jpeg'],key = 2)

            if (image_file1 and image_file2) is not None:
                my_image1 = Image.open(image_file1)
                my_image2 = Image.open(image_file2)
                new_image1 = np.array(my_image1.convert('RGB'))
                new_image2 = np.array(my_image2.convert('RGB'))
                new_image1 = cv2.resize(new_image1,(0,0),None,0.2,0.2)
                new_image2 = cv2.resize(new_image2,(0,0),None,0.2,0.2)
                images = []
                images.append(new_image1)
                images.append(new_image2)
                stitcher = cv2.Stitcher.create()
                (status,result) = stitcher.stitch(images)
                result = cv2.resize(result,(width,height))
                if status == cv2.STITCHER_OK:
                    st.text("Panorama Generated")
                    st.image(result)
                else:
                    st.text("Panorama Generation Failed")
                result = Image.fromarray(result)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    result = result.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    result = result.rotate(angle2)
                elif rotate == "Clockwise 180":
                    result = result.rotate(angle3)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)


        elif total == "3":
            image_file1 = st.file_uploader("Upload Image 1",type = ['jpg','png','jpeg'],key = 1)
            image_file2 = st.file_uploader("Upload Image 2",type = ['jpg','png','jpeg'],key = 2)
            image_file3 = st.file_uploader("Upload Image 3",type = ['jpg','png','jpeg'],key = 3)
            if (image_file1 and image_file2 and image_file3) is not None:
                my_image1 = Image.open(image_file1)
                my_image2 = Image.open(image_file2)
                my_image3 = Image.open(image_file3)
                new_image1 = np.array(my_image1.convert('RGB'))
                new_image2 = np.array(my_image2.convert('RGB'))
                new_image3 = np.array(my_image3.convert('RGB'))
                new_image1 = cv2.resize(new_image1,(0,0),None,0.2,0.2)
                new_image2 = cv2.resize(new_image2,(0,0),None,0.2,0.2)
                new_image3 = cv2.resize(new_image3,(0,0),None,0.2,0.2)
                images = []
                images.append(new_image1)
                images.append(new_image2)
                images.append(new_image3)
                stitcher = cv2.Stitcher.create()
                (status,result) = stitcher.stitch(images)
                result = cv2.resize(result,(width,height))
                if status == cv2.STITCHER_OK:
                    st.text("Panorama Generated")
                    st.image(result)
                else:
                    st.text("Panorama Generation Failed")
                result = Image.fromarray(result)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    result = result.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    result = result.rotate(angle2)
                elif rotate == "Clockwise 180":
                    result = result.rotate(angle3)
                st.markdown(get_image_download_link(result), unsafe_allow_html = True)

    elif option == "Document Scanner":
        st.title("Scan your Document here :")
        st.subheader("Upload your Image")
        image_file = st.file_uploader("Upload Image",type = ['jpg','png','jpeg'])
        activity = ["Original","Scanned"]
        choices = st.sidebar.radio("Select choice : ",activity)
        brightness = st.sidebar.slider("Brightness",1,5)
        Contrast = st.sidebar.slider("Contrast",1,5)
        Sharpness = st.sidebar.slider("Sharpness",1,15)
        if image_file is not None:
            new_image = Image.open(image_file)
            new_image1 = np.array(new_image.convert('RGB'))
            ratio = new_image1.shape[0]/500.0
            orig = new_image1.copy()
            new_image1 = imutils.resize(new_image1,height = 500)
            gray = cv2.cvtColor(new_image1,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(5,5),0)
            edged = cv2.Canny(gray,75,200)
            cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

            for c in cnts:
                peri = cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,0.02*peri,True)

                if len(approx) == 4:
                    screenCnt = approx
                    break

            x = approx[0][0][0]
            y = approx[0][0][1]
            x1 = approx[1][0][0]
            y1 = approx[1][0][1]
            x2 = approx[2][0][0]
            y2 = approx[2][0][1]
            x3 = approx[3][0][0]
            y3 = approx[3][0][1]
            cv2.drawContours(new_image1, [approx],-1,(0,255,0),2)

            pts1 = np.float32([[x,y],[x1,y1],[x2,y2],[x3,y3]])
            pts2 = np.float32([[width,0],[0,0],[0,height],[width,height]])
            matrix = cv2.getPerspectiveTransform(pts1,pts2)

            imgOutput = cv2.warpPerspective(new_image1,matrix,(width,height))
            imgOutput = cv2.resize(imgOutput,(width,height))

            if choices == "Original":
                st.title("Original Image")
                enhancer = ImageEnhance.Brightness(new_image)
                new_image = enhancer.enhance(brightness)
                enhancer = ImageEnhance.Contrast(new_image)
                new_image = enhancer.enhance(Contrast)
                enhancer = ImageEnhance.Sharpness(new_image)
                new_image = enhancer.enhance(Sharpness)
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                new_image = Image.fromarray(new_image)

                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    new_image = new_image.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    new_image = new_image.rotate(angle2)
                elif rotate == "Clockwise 180":
                    new_image = new_image.rotate(angle3)

                st.image(new_image)
                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)

            elif choices == "Scanned":
                st.title("Scanned Image")
                imgOutput = Image.fromarray(imgOutput, 'RGB')
                enhancer = ImageEnhance.Brightness(imgOutput)
                imgOutput = enhancer.enhance(brightness)
                enhancer = ImageEnhance.Contrast(imgOutput)
                imgOutput = enhancer.enhance(Contrast)
                enhancer = ImageEnhance.Sharpness(imgOutput)
                imgOutput = enhancer.enhance(Sharpness)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    imgOutput = imgOutput.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    imgOutput = imgOutput.rotate(angle2)
                elif rotate == "Clockwise 180":
                    imgOutput = imgOutput.rotate(angle3)

                st.image(imgOutput)
                st.markdown(get_image_download_link(imgOutput), unsafe_allow_html = True)




    elif option == "Feature Detection":
        st.title("Detect Features in your Image")
        st.subheader("Upload your image")
        image_file = st.file_uploader("Upload Image",type = ['jpg','png','jpeg'])
        activity = ["Original","Face","Eyes","Smiles"]
        opt = st.sidebar.radio("Detect Feature: ",activity)

        if image_file is not None:
            if opt == "Original":
                new_image = Image.open(image_file)
                st.title("Original Image")
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                st.image(new_image)
                new_image = Image.fromarray(new_image)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    new_image = new_image.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    new_image = new_image.rotate(angle2)
                elif rotate == "Clockwise 180":
                    new_image = new_image.rotate(angle3)

                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)

            elif opt == "Face":
                new_image = Image.open(image_file)
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                new_image1 = cv2.cvtColor(new_image,cv2.COLOR_RGB2GRAY)
                faces = face_cascade.detectMultiScale(new_image1,1.1,10)

                if faces is ():
                    print("No faces found")

                else:
                    for (x,y,w,h) in faces:
                        cv2.rectangle(new_image,(x,y),(x+w,y+h),(127,0,255),2)

                    st.title("Face Detected")
                    new_image = cv2.resize(new_image,(width,height))
                    st.image(new_image)
                    st.success("Found {} faces".format(len(faces)))
                new_image = Image.fromarray(new_image)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    new_image = new_image.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    new_image = new_image.rotate(angle2)
                elif rotate == "Clockwise 180":
                    new_image = new_image.rotate(angle3)
                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)

            elif opt == "Eyes":
                new_image = Image.open(image_file)
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                new_image1 = cv2.cvtColor(new_image,cv2.COLOR_RGB2GRAY)
                faces = face_cascade.detectMultiScale(new_image1,1.1,10)

                if faces is ():
                    print("No eyes found")

                else:
                    for (x,y,w,h) in faces:
                        roi_gray = new_image1[y:y+h,x:x+h]
                        roi_color = new_image[y:y+h,x:x+h]
                        eyes = eye_cascade.detectMultiScale(roi_gray,1.1,10)
                        for(ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(127,0,255),2)

                    st.title("Eyes Detected")
                    new_image = cv2.resize(new_image,(width,height))
                    st.image(new_image)
                    st.success("Found {} eyes".format(2*len(faces)))
                new_image = Image.fromarray(new_image)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    new_image = new_image.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    new_image = new_image.rotate(angle2)
                elif rotate == "Clockwise 180":
                    new_image = new_image.rotate(angle3)
                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)

            elif opt == "Smiles":
                new_image = Image.open(image_file)
                new_image = np.array(new_image.convert('RGB'))
                new_image = cv2.resize(new_image,(width,height))
                new_image1 = cv2.cvtColor(new_image,cv2.COLOR_RGB2GRAY)
                faces = face_cascade.detectMultiScale(new_image1,1.1,10)

                if faces is ():
                    print("No Smiles found")

                else:
                    for (x,y,w,h) in faces:
                        roi_gray = new_image1[y:y+h,x:x+h]
                        roi_color = new_image[y:y+h,x:x+h]
                        smiles = smile_cascade.detectMultiScale(roi_gray,1.8,20)
                        for(sx,sy,sw,sh) in smiles:
                            cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(127,0,255),2)

                    st.title("Smile Detected")
                    new_image = cv2.resize(new_image,(width,height))
                    st.image(new_image)
                    st.success("Found {} smiles".format(len(faces)))

                new_image = Image.fromarray(new_image)
                if rotate == "Selection Option":
                    pass
                elif rotate == "Clockwise 90":
                    new_image = new_image.rotate(angle1)
                elif rotate == "Anticlockwise 90":
                    new_image = new_image.rotate(angle2)
                elif rotate == "Clockwise 180":
                    new_image = new_image.rotate(angle3)
                st.markdown(get_image_download_link(new_image), unsafe_allow_html = True)





if __name__ == "__main__":
    main()
