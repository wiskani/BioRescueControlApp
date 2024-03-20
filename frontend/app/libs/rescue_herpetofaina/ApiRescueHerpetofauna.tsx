export const GetTransectHerpetofaunaWithSpecies=async(props:Token): Promise < TransectHerpetoWithSpecies[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL}:8080/api/transect_herpetofauna_with_species_and_count`,
                        requestOptions
                        );
        const data = await response.json();
        return data;
}
