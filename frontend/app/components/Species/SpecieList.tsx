import { useState } from "react";
import SpecieItem from "./SpecieItem";

interface SpecieListProps {
  species: SpecieItemData[];
}

const SpecieList: React.FC<SpecieListProps> = ({species}) => {
    console.log(species);
  const [searchSpecie, setSearchSpecie] = useState('');

  //function to filter the species
  const filteredSpecies = species.filter(specie => 
    specie.specie_name.toLowerCase().includes(searchSpecie.toLowerCase())
  )
  return (
        <div className="container mx-auto px-4 py-20">
          <h2 className="text-center sm:text-4xl text-2xl font-bold tracking-tight text-gray-800">Especies</h2>
          <div className="flex my-4 content-center justify-center">
            <input
              type="text"
              placeholder="Buscar por nombre cientifico"
              className="w-60 p-2 border rounded"
              value={searchSpecie}
              onChange={e => setSearchSpecie(e.target.value)}
            />
          </div>
          { species.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {filteredSpecies.map((specieData) => (
                    <SpecieItem key={specieData.specie_name} {...specieData} />
                ))}
            </div>
            ) : (
            <div className="text-center">
            <p>No hay especies registradas</p>
            </div>
            )
            }
        </div>
    );
}

export default SpecieList;
