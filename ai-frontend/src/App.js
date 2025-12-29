import {useState, useRef} from 'react';
import * as apiClient from './modules/apiClient';

import Grid from '@mui/material/Grid';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import Button from '@mui/material/Button';

import Canvas from './components/Canvas';
import './css/App.css';

function App() {
  const [state, setState] = useState('canvas');
  const prediction = useRef();

  const submit = async (drawing) => {
    if (!drawing[0]) return;
    if (state == 'loading') {
      return;
    }
    setState('loading');

    const result = await apiClient.getPrediction(drawing);
    if (result) {
      prediction.current = result.prediction;
    }
    setState('results');
  }

  const reset = () => {
    setState('canvas');
  }

  return <>
    <div className='app-header'>
      <h1>Sketch!</h1>
      <h2>Sketch something and our AI will determine what it is.</h2>
    </div>

    {state == 'loading' &&
      <Grid container direction="column" alignItems="center" gap={5} marginTop={20}>
        <CircularProgress color="info" size="6rem"/>
        <h2>Loading Prediction...</h2>
        <Alert severity="info">While you wait, did you know that this app was made by Jack Goeders?</Alert>
      </Grid>
    }

    {prediction.current && state == 'results' &&
      <Grid container direction="column" alignItems="center" gap={2} marginTop={35}>
        <h2 className='prediction-container'>We predict that you drew: {prediction.current}</h2>
        <Button variant='contained' onClick={reset} size='large' startIcon={<RestartAltIcon/>}>
          Reset
        </Button>
      </Grid>
    }

    {state == 'canvas' &&
      <Canvas
        onSubmit={submit}
      />
    }
  </>
}

export default App;
