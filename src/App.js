import './App.css';
import React, { useEffect, useState } from 'react'
function App() {
 const [source_bucket_name,setsource_bucket_name]=useState("");
 const [source_account_id,setsource_account_id]=useState("");
 const [source_account_access_key,setsource_account_access_key]=useState("");
 const [source_account_secret_access_key,setsource_account_secret_access_key]=useState("");
 const [destination_bucket_name,setdestination_bucket_name]=useState("");
 const [destination_account_id,setdestination_account_id]=useState("");
 const [destination_account_username,setdestination_account_username]=useState("");
 const [destination_account_access_key,setdestination_account_access_key]=useState("");
 const [destination_account_secret_access_key,setdestination_account_secret_access_key]=useState("");
 const [file_name,setfile_name]=useState("");

function saveData()
{
  let data={source_bucket_name,source_account_id,source_account_access_key,source_account_secret_access_key,destination_bucket_name, destination_account_id, destination_account_username, destination_account_access_key, destination_account_secret_access_key, file_name}
// console.warn(data);
  fetch("http://127.0.0.1:5000/add", {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body:JSON.stringify(data)
  }).then((resp)=>{
    // console.warn("resp",resp);s
    resp.json().then((result)=>{
      console.warn("result",result)
      alert(result.error ? result.error : result.result)
    })
  })
}
  return (
    <div class="App">
      <h1>Try Copying Data Between S3 Buckets Of Different AWS Accounts </h1>  
      <h3>Enter Required Credentials</h3>
      {/* <div>Enter source bucket name</div> */}
      <input placeholder='Enter source bucket name' type="text" name="source_bucket_name" value={source_bucket_name} onChange={(e)=>{setsource_bucket_name(e.target.value)}}  /> <br /> 
      {/* <div>Enter source account id</div> */}
      <input placeholder='Enter source account id' type="password" name="source_account_id"  value={source_account_id} onChange={(e)=>{setsource_account_id(e.target.value)}} /> <br /> 
      {/* <div>Enter source account access key</div> */}
      <input placeholder='Enter source account access key' type="password" name="source_account_access_key"  value={source_account_access_key} onChange={(e)=>{setsource_account_access_key(e.target.value)}}/> <br /> 
      {/* <div>Enter source account secret access key</div> */}
      <input placeholder='Enter source account secret access key' type="password" name="c" value={source_account_secret_access_key} onChange={(e)=>{setsource_account_secret_access_key(e.target.value)}}  /> <br /> 
      {/* <div>Enter destination bucket name</div> */}
      <input placeholder='Enter destination bucket name' type="text" name="destination_bucket_name" value={destination_bucket_name} onChange={(e)=>{setdestination_bucket_name(e.target.value)}}  /> <br /> 
      {/* <div>Enter destination account id</div> */}
      <input placeholder='Enter destination account id' type="password" name="destination_account_id" value={destination_account_id} onChange={(e)=>{setdestination_account_id(e.target.value)}}  /> <br /> 
      {/* <div>Enter destination account username</div> */}
      <input placeholder='Enter destination account username' type="text" name="destination_account_username" value={destination_account_username} onChange={(e)=>{setdestination_account_username(e.target.value)}}  /> <br /> 
      {/* <div>Enter destination account access key</div> */}
      <input placeholder='Enter destination account access key' type="password" name="destination_account_access_key" value={destination_account_access_key} onChange={(e)=>{setdestination_account_access_key(e.target.value)}}  /> <br /> 
      {/* <div>Enter destination account secret access key</div> */}
      <input placeholder='Enter destination account secret access key' type="password" name="destination_account_secret_access_key" value={destination_account_secret_access_key} onChange={(e)=>{setdestination_account_secret_access_key(e.target.value)}}  /> <br /> 
      {/* <div>Enter a file name which you want to copy from source to destination</div> */}
      <input placeholder='Enter a file name which you want to copy from source to destination' type="text" name="file_name" value={file_name} onChange={(e)=>{setfile_name(e.target.value)}}  /> <br /> 

      <button type="button" onClick={saveData} >Proceed</button>
    </div>
  );
}
export default App;