export default function Page({ params} : { params: { specie_id: number } }) {
        return (
            <div>
                <h1>esta es una prueba{params.specie_id}</h1>
            </div>
        )
        }

