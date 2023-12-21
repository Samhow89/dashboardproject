import useFetch from "./useFetch";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const Listprojects = () => {

    const { data, isPending, error } = useFetch('http://127.0.0.1:5000/projects/all')

    const [totalProjects, setTotalProjects] = useState(0)


    useEffect(() => {
        data && setTotalProjects(data.length)
    }, [data]);

    return ( 
    <>
        { error && <div>{ error }</div> }
        { isPending && <div>Loading...</div> }
        {data && (
            <ul>
                <h1>Total projects: {totalProjects}</h1>
                {data.map(data => (
                    <div className="project-preview" key={data.ID}>
                    <Link to={`/project/${data.ID}`}>
                    <h2>Name:</h2>
                    <p>{data.Name}</p>
                    </Link>
                    </div>
                ))}
        
            </ul>
        )}  
    </>

        
     );
}
 
export default Listprojects;