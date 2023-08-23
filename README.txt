Problems:
- split_seq returns images that are too dark and don't even look like thermals.
  It conflicts with the output from FLIR Studio, which gives frames of the thermal ".seq" video.
- You can't do anything useful on the free version of FLIR Studio.
- Colormapping the grayscale images helps, but a lot of thermal info is lost and/or warped.

Options:
- https://github.com/detecttechnologies/Thermal-Image-Analysis
- FLIR Tools. Can't install it on this machine; need to do it on my own laptop and put it on a USB.

Installation: 
- Follow the steps here for the FLIR File SDK: https://flir.custhelp.com/app/answers/detail/a_id/3504/~/getting-started-with-flir-science-file-sdk-for-python
  Make sure you check your python version and install the respective FileSDK.


Results:
- Flirpy's `split_seq` gives grayscale images. The library itself is unusable due to nonexistant documentation.
- FLIR SDK also gives grayscale images, even with superframes. Using a colormap doesn't really help. 
- Based on [this](https://flir.custhelp.com/app/answers/detail/a_id/3036/related/1), FLIR Tools isn't any more helpful than FLIR Thermal Studio.


Discussion:
FLIRPY
Why is it that only the ~first image of each .seq video actually shows something, while all the rest are dark?
I think it's because of the way "superframing" works. It takes like 4 pictures at different 
exposure rates and creates a final image that is a superimposition of those four such that 
contrast and visibility are maximized while retaining thermal information. But then shouldn't
that mean that everything fourth-ish picture is actually viewable? Right now, only the *first*
one is. 

SDK
All the images look the same, and nothing like the thermal image, so even if I were to use a
colormap it wouldn't recreate the original.


Conclusion:
`split_seqs` produces grayscale images which I can then colormap to look like something perfect.
It's not perfect, because a lot of images come out blank, but if I can remove those then we have
a working dataset that we can feed to a machine learning model. 

There's the issue of annotation, of course. An expert who can identify a flaw from the .seq video
might not be able to from these colormapped images since they don't look the 3xact same as the .seq frames;
a lot of visual info is lost. 

I've been trying to solve that problem, but no tool that converts .seq videos (that I've found) seems able to 
solve it.