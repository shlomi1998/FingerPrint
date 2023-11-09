import React, { useState } from "react";
import Slider from "@mui/material/Slider";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import { AiOutlineClose, AiOutlineCloseSquare } from "react-icons/ai";
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@mui/material";

interface SliderState {
  rotateImage: number;
  brightness: number;
  sharpness: number;
  cleanNoise: number;
  cleanFingerprint: number;
  matrixSize: number;
}

const initialSliderState: SliderState = {
  rotateImage: 10,
  brightness: 10,
  sharpness: 10,
  cleanNoise: 10,
  cleanFingerprint: 10,
  matrixSize: 10,
};

const ImageRecognition = () => {
  const [finger, setFinger] = useState("");
  const [hand, setHand] = useState("");
  const [accuracyLevel, setAccuracyLevel] = useState<any>(1);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(
    "./images/loadImg.webp"
  );
  const [isErrorDialogOpen, setIsErrorDialogOpen] = useState(false);

  const [sliderState, setSliderState] =
    useState<SliderState>(initialSliderState);

  const handleFinger = (event: SelectChangeEvent) => {
    setFinger(event.target.value);
  };

  const handleHand = (event: SelectChangeEvent) => {
    setHand(event.target.value);
  };

  const handleAccuracyLevel = (event: SelectChangeEvent) => {
    setAccuracyLevel(event.target.value);
    console.log(accuracyLevel)
  };

  const handleLoadImageClick = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const imageUrl = URL.createObjectURL(file);
        setSelectedImage(imageUrl);
        setImageLoaded(true);
      }
    };
    input.click();
  };

  const resetImage = () => {
   setImageLoaded(false)
  };

  const handleRotateImageChange = (event: Event, newValue: number | number[]) => {
    setSliderState((prev) => ({ ...prev, rotateImage: newValue instanceof Array ? newValue[0] : newValue }));
    console.log(sliderState.rotateImage)
  };

  const handleBrightnessChange = (event: Event, newValue: number | number[]) => {
    setSliderState((prev) => ({ ...prev, brightness: newValue instanceof Array ? newValue[0] : newValue }));
    console.log(sliderState.brightness)
  };

  const handleSharpnessChange = (event: Event, newValue: number | number[]) => {
    setSliderState((prev) => ({ ...prev, sharpness: newValue instanceof Array ? newValue[0] : newValue }));
  };

  const handleCleanNoiseChange = (event: Event, newValue: number | number[]) => {
    setSliderState((prev) => ({ ...prev, cleanNoise: newValue instanceof Array ? newValue[0] : newValue }));
    console.log(sliderState.cleanNoise)
  };

  const handleCleanFingerprintChange = (event: Event, newValue: any) => {
    setSliderState((prev) => ({ ...prev, cleanFingerprint: newValue instanceof Array ? newValue[0] : newValue }));
    console.log(sliderState.cleanFingerprint)
  };
  const handleMatrixSizeChange = (event: Event, newValue: any) => {
    setSliderState((prev) => ({ ...prev, matrixSize: newValue instanceof Array ? newValue[0] : newValue }));
    console.log(sliderState.matrixSize)
  };

 
  const validateAndSaveToDb = () => {
    if (!finger || !hand) {
      // אם אין בחירה באצבע או יד, פתח את חלון הדו-שיח של השגיאה
      setIsErrorDialogOpen(true);
    } else {
      // שמור במסד הנתונים
      // ... קוד לשמירה במסד הנתונים ...
    }
  };
  

  // React.useEffect(() => {
  //   console.log(accuracyLevel); // this will now reflect the updated state
  // }, [accuracyLevel]); 
  return (
    <div className=" z-50 fixed  rounded-md flex w-[640px] h-[620px]  bg-[#c4f9f4e8] ">
      <div className="text-slate-800 hover:text-[black]  cursor-pointer z-[50]  absolute right-2 top-2  ">
        <AiOutlineClose className=" text-2xl cursor-pointer hover:text-[25px]  " />
      </div>

      <div className=" w-[100%] h-[100%] relative -left-2 -top-6 flex-1 flex flex-col  items-center justify-center gap-2 ">
        <div className="relative -top-28">
          <div className="mb-3 w-[110PX] h-[50px] ">
            <button
              onClick={handleLoadImageClick}
              className="shadow-md shadow-gray-800 text-white w-full h-full rounded-md bg-slate-950 hover:bg-black border-0 "
            >
              Load image
            </button>
          </div>
          <div className="mb-3  w-[110PX] h-[50px]">
            <button className="shadow-md shadow-gray-800 text-white w-full h-full rounded-md bg-slate-950 hover:bg-black border-0 ">
              Take a picture
            </button>
          </div>
          <div className="mb-3 w-[110PX] h-[50px]">
            <button onClick={resetImage}  className="shadow-md shadow-gray-800 text-white w-full h-full rounded-md bg-slate-950 hover:bg-black  border-0 ">
              Reset image
            </button>
          </div>
        </div>
        <div className="relative bottom-24  ">
          <div className="mb-3 w-[110px] h-[50px] ">
            <FormControl
              variant="standard"
              sx={{ m: 1, minWidth: 135, marginBottom: 2 }}
            >
              <InputLabel id="demo-simple-select-standard-label">
                Finger
              </InputLabel>
              <Select
                labelId="demo-simple-select-standard-label"
                id="demo-simple-select-standard"
                value={finger}
                onChange={handleFinger}
                label="Finger"
              >
                <MenuItem value={"thumb"}>Thumb</MenuItem>
                <MenuItem value={"finger"}>Finger</MenuItem>
              </Select>
            </FormControl>
            <br />
            <FormControl
              variant="standard"
              sx={{ m: 1, minWidth: 135, marginBottom: 2 }}
            >
              <InputLabel id="demo-simple-select-filled-label">Hand</InputLabel>
              <Select
                labelId="demo-simple-select-filled-label"
                id="demo-simple-select-filled"
                value={hand}
                onChange={handleHand}
                label="Hand"
              >
                <MenuItem value={"right"}>Right</MenuItem>
                <MenuItem value={"left"}>Left</MenuItem>
              </Select>
            </FormControl>
            <br />
            <FormControl variant="standard" sx={{ m: 1, minWidth: 135 }}>
              <InputLabel id="demo-simple-select-standard-label">
                Accuracy level
              </InputLabel>
              <Select
                labelId="demo-simple-select-standard-label"
                id="demo-simple-select-standard"
                value={accuracyLevel}
                onChange={handleAccuracyLevel}
                label="Accuracy level"
              >
                <MenuItem value={1}>1%</MenuItem>
                <MenuItem value={10}>10%</MenuItem>
                <MenuItem value={20}>20%</MenuItem>
                <MenuItem value={30}>30%</MenuItem>
                <MenuItem value={40}>40%</MenuItem>
                <MenuItem value={50}>50%</MenuItem>
                <MenuItem value={60}>60%</MenuItem>
                <MenuItem value={70}>70%</MenuItem>
                <MenuItem value={80}>80%</MenuItem>
                <MenuItem value={90}>90%</MenuItem>
                <MenuItem value={100}>100%</MenuItem>
              </Select>
            </FormControl>
          </div>
        </div>
      </div>
      <div className="flex-1 flex flex-col items-center justify-center gap-2 relative -top-10">
        <div className=" rounded-md relative top-7 w-[270px] h-[180px] bg-[#000000] border-2 border-[#000]">
          {imageLoaded ? (
            <>
              <h2 className="p-2 text-[12px] font-mono mx-auto mt-2 text-white overflow-hidden">
                {selectedImage}
              </h2>
              <img
                className="${} mx-auto mt-1 rounded-sm w-[100px] h-[100px] cursor-pointer "
                src={selectedImage || ""}
                alt=""
              />
            </>
          ) : (
            <>
              <h2 className="font-mono relative mt-3 left-[28%] text-white">
                No image loaded
              </h2>
              <img
                className=" mx-auto mt-0 rounded-sm w-[90%] h-[80%]  "
                src={"./images/loadImg.webp"}
                alt=""
              />
            </>
          )}
        </div>
        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px] mt-[40px] ">
          <span className="absolute font-bold text-sm  ">Rotate Image</span>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={handleRotateImageChange}
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>
        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px] ">
          <h1 className="absolute  font-bold  text-sm">Brightness</h1>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={ handleBrightnessChange}
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>

        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px] ">
          <h1 className=" absolute font-bold  text-sm">Sharpness</h1>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={handleSharpnessChange }
            
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>
        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px] ">
          <h1 className="absolute font-bold  text-sm">CleanNoise</h1>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={handleCleanNoiseChange}
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>

        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px] ">
          <h1 className="absolute font-bold  text-sm">Clean fingerprint</h1>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={ handleCleanFingerprintChange}
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>
        <div className="pl-1 flex items-center space-x-[130px] w-[270px] h-[40px]">
          <h1 className="absolute font-bold text-sm">MatrixSize</h1>
          <Slider
            className="flex-grow"
            aria-label="Temperature"
            defaultValue={0}
            valueLabelDisplay="auto"
            step={10}
            marks
            min={0}
            max={100}
            onChange={handleMatrixSizeChange}
            sx={{
              "& .MuiSlider-thumb": {
                backgroundColor: "black",
                width: 20,
                height: 20,
                "&:hover": {
                  backgroundColor: "darkblue",
                },
              },
              "& .MuiSlider-track": {
                backgroundColor: "black",
              },
              "& .MuiSlider-rail": {
                backgroundColor: "black",
              },
            }}
          />
        </div>
      </div>

      <div className="w-full flex justify-center space-x-20 absolute bottom-4">
        <div className="shadow-md shadow-gray-800 w-[110px] h-[52px] bg-slate-950 hover:bg-black border-2 border-[#000] rounded-md">
          <button className=" text-white font-mono w-full h-full">
            C2C
          </button>
        </div>
        <div className="shadow-md shadow-gray-800 w-[110px] h-[52px] bg-slate-950 hover:bg-black border-2 border-[#000] rounded-md ">
          <button className="text-[15px] text-white font-mono w-full h-full">
            Find match in DB
          </button>
        </div>
        <div className=" shadow-md shadow-gray-800 w-[110px] h-[52px] bg-slate-950 hover:bg-black border-2 border-[#000] rounded-md">
        <button onClick={validateAndSaveToDb} className=" text-white font-mono w-full h-full">
        Save in DB
      </button>
     </div>
      {/* דו-שיח של הודעת השגיאה */}
      <Dialog
        open={isErrorDialogOpen}
        onClose={() => setIsErrorDialogOpen(false)}
        sx={{
          '& .MuiPaper-root': {
            bgcolor: 'black',
            color: 'white',
          },
        }}
      >
        <DialogTitle sx={{ color: 'white' }}
        >Warning</DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ color: 'white' }}>
            No hand or finger was selected
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button sx={{ color: '#00ffe5' }} onClick={() => setIsErrorDialogOpen(false)}>אישור</Button>
        </DialogActions>
      </Dialog>
        </div>
      </div>
   
  );
};

export default ImageRecognition;

