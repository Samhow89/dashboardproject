import { useParams } from "react-router-dom";
import useFetch from "./useFetch";
import { useEffect } from "react";
import { useState } from "react";

const Projectdetail = () => {

    const { id } = useParams()

    const { data, isPending, error } = useFetch(`http://127.0.0.1:5000/projects/${id}`)

    const [totalInstances, setTotalInstances] = useState(0)


    useEffect(() => {
        data && setTotalInstances(data.length)
    }, [data]);

    
    return (  
        <>
        { error && <div>{ error }</div> }
        { isPending && <div>Loading...</div> }
    
        {data && totalInstances > 0 && (
    
            <ul>
                
                <h2>Instances in {id}:</h2>
                {data.map(data => (
                    <div className="project-preview2" key={data.ID}>
                    <h2>{data.Name}</h2>
                    <p>Status: {data.Status}</p>
                    <p>Internal IP: {data.Internal_IP}</p>
                    <p>CPU Utilization: {data.CPU_Utilization}</p>
                    </div>
                ))}
                <h3>Total instances: {totalInstances}</h3>
            </ul>
        )} 


        {totalInstances <= 0 && !isPending &&(
            
            <ul>
                <h2>No instances in project!</h2>
                
            </ul>
        )} 

    </>
    );
}
 
export default Projectdetail;