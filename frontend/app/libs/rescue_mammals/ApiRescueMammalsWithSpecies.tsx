
export const GetRescueMammalsWithSpecies =
        async (props: Token): Promise<RescueMammalsWithSpecieData[]>=> {
        const requestOptions = {
        method: 'GET',
        headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
        },
        };
        const response = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL}:8080/api/rescue_mammals_species`,
                        requestOptions
                        );
        const data = await response.json();
        return data;
        }
