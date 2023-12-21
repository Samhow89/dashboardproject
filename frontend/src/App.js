import Navbar from './navbar';
import Listprojects from './listprojects';
import Home from './home';
import Projectdetail from './projectdetail';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {


  return (
    <Router>
      <div className="App">

        <Navbar />

        <div className="content">
        
        <Switch>

          <Route exact path="/">
            <Home/>
          </Route>

          <Route exact path="/projects">
            <Listprojects/>
          </Route>


          <Route path="/project/:id">
            <Projectdetail/>
          </Route>


        </Switch>

        
        </div>
      </div>
    </Router>
  );
}

export default App;

