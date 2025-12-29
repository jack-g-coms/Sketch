import {useState, useRef} from 'react';

import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack'
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';

import '../css/Canvas.css';

// Top left is (0, 0).
// Drawing is a set of strokes which are [[x1, x2, x3, ...], [y1, y2, y3, ...]] = a Stroke.
// (x[i], y[i]) is one point in time.
function Canvas({onSubmit}) {
    const canvasRef = useRef(null);

    const [drawing, setDrawing] = useState([]);
    const [activeStroke, setActiveStroke] = useState(false);
    const [stroke, setStroke] = useState([[], []]);

    const getRelativePosition = (event) => {
        const canvas = canvasRef.current;
        const rect = event.target.getBoundingClientRect();
        
        const x = ((event.clientX - rect.left) / rect.width) * canvas.width;
        const y = ((event.clientY - rect.top) / rect.height) * canvas.height;

        return [Math.max(Math.round(x), 0), Math.max(Math.round(y), 0)];
    }

    const finishStroke = () => {
        setDrawing((old) => {
            const newStroke = [...old, stroke];

            setStroke([[], []]);
            setActiveStroke(false);

            return newStroke;
        });
    }

    const captureStroke = (event) => {
        if (activeStroke) {
            const [x, y] = getRelativePosition(event);

            setStroke((old) => {
                const xPoints = old[0];
                const yPoints = old[1];

                if (xPoints.length != 0 && yPoints.length != 0) {
                    const lastX = xPoints[xPoints.length - 1];
                    const lastY = yPoints[yPoints.length - 1];

                    if (lastX == x || lastY == y) {
                        return old;
                    }

                    const ctx = canvasRef.current.getContext('2d');
                    ctx.beginPath();
                    ctx.moveTo(lastX, lastY);
                    ctx.lineTo(x, y);
                    ctx.strokeStyle = 'black';
                    ctx.lineWidth = 2;
                    ctx.lineCap = 'round';
                    ctx.stroke();
                }

                const newXPoints = [...xPoints, x];
                const newYPoints = [...yPoints, y];

                return [newXPoints, newYPoints];
            });
        }
    }

    const mouseDown = (event) => {
        if (canvasRef.current) {
            if (activeStroke) {
                finishStroke();
            }
            setActiveStroke(true);
        }
    }

    const mouseUp = (event) => {
        if (activeStroke) {
            finishStroke();
        }
    }

    const reset = () => {
        setDrawing([]);
        setActiveStroke(false);
        setStroke([[], []]);
    }

    const clear = () => {
        const canvas = canvasRef.current;
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            reset();
        }
    }

    const submit = () => {
        onSubmit(drawing);
        clear();
    }

    return <>
        <canvas
            className='canvas'
            ref={canvasRef}
            onMouseDown={mouseDown}
            onMouseMove={captureStroke}
            onMouseUp={mouseUp}
            height='256'
            width='256'
        />

        <Stack direction="row" spacing={1}>
            <Button variant='contained' onClick={submit} size='large' startIcon={<SendIcon/>}>
                Submit  
            </Button>
            <Button variant='outlined' onClick={clear} size='large' startIcon={<DeleteIcon/>}>
                Clear Drawing 
            </Button>
        </Stack>  
    </>
}

export default Canvas;