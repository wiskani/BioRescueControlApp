export const GetRescueHerpetofauna=async(props:Token): Promise <FloraRescueData[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        'http://localhost:8080/api/transect_herpetofauna',
                        requestOptions
                        );
        const data = await response.json();
        return data;
}

export const GetTransectHerpetofauna=async(props:Token): Promise < TransectHerpetofaunaData[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        'http://localhost:8080/api/transect_herpetofauna',
                        requestOptions
                        );
        const data = await response.json();
        return data;
}

export const GetTransectHerpetofaunaWithSpecies=async(props:Token): Promise < TransectHerpetoWithSpecies[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        'http://localhost:8080/api/transect_herpetofauna_with_species_and_count',
                        requestOptions
                        );
        const data = await response.json();
        return data;
}
