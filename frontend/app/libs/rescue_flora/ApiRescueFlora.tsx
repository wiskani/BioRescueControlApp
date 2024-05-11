interface TokenWithNumberEpiphte extends Token {
    epiphyte_number:string
}

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
    try{
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
        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(errorDetails.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}

export const GetRelocationFloraSpecie=async(props:Token): Promise <FloraRelocationWithSpecieData[]>=> {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/flora_relocation_with_specie`,
            requestOptions
        );
        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(errorDetails.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}

export const GetRescueFloraSpecieByEpiphyteNumber=async(
    props:TokenWithNumberEpiphte
): Promise <FloraRescueSpeciesData>=> {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/flora_rescue_species/${props.epiphyte_number}`,
            requestOptions
        );
        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(errorDetails.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}

export const GetRelocationFloraSpecieByEpiphyteNumber=async(
    props:TokenWithNumberEpiphte
): Promise <FloraRelocationWithSpecieData | {message : string}>=> {
    try{
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/flora_relocation_with_specie/${props.epiphyte_number}`,
            requestOptions
        );
        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(errorDetails.detail || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}
