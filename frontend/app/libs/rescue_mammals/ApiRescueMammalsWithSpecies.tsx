interface TokenWithRescueNumber extends Token {
    cod:string
}

export const GetRescueMammalsWithSpecies =
async (props: Token): Promise<RescueMammalsWithSpecieData[]>=> {
    try {
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

export const GetRealeaseMammalsWithSpecies =
async (props: Token): Promise<ReleaseMammalsWithSpecieData[]>=> {
    try {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/release_mammals_species`,
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

export const GetRescueMammalsWithSpecieByNumber =
async (props: TokenWithRescueNumber): Promise<RescueMammalsWithSpecieExtendedData>=> {
    try {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/rescue_mammals_species/${props.cod}`,
            requestOptions
        );

        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(
                errorDetails.detail || `HTTP error! status: ${response.status}`
            );
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}

export const GetReleaseMammalsWithSpecieByNumber =
async (props: TokenWithRescueNumber): Promise<ReleaseMammalsWithSpecieData>=> {
    try {
        const requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + props.token ,
            },
        };
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}:8080/api/release_mammals_species/${props.cod}`,
            requestOptions
        );

        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(
                errorDetails.detail || `HTTP error! status: ${response.status}`
            );
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        throw error;  // Re-throw the error to be handled by the caller
    }
}

