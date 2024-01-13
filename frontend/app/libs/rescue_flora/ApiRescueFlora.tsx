
export const GetRescueFlora=async(props:Token): Promise <FloraRescueData[]>=> {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}:8080/api/rescue_flora`,
    requestOptions
  );
  const data = await response.json();
  return data;
}


export const GetRescueFloraSpecie=async(props:Token): Promise <FloraRescueSpeciesData[]>=> {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + props.token ,
    },
  };
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}:8080/api/flora_rescue_species`,
    requestOptions
  );
  const data = await response.json();
  return data;
}

