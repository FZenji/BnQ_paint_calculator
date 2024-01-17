"use client";
import Image from "next/image";
import { useState } from "react";
import { Select, SelectSection, SelectItem } from "@nextui-org/select";
import { Button } from "@nextui-org/button";

export default function Home() {
  let maxWalls = 10;
  let minWalls = 0;
  let maxCoats = 3;
  let minCoats = 1;
  let brands = [
    { label: "Cheap", value: "cheap", description: "5 sqm/L" },
    { label: "Medium", value: "medium", description: "10 sqm/L" },
    { label: "Expensive", value: "expensive", description: "15 sqm/L" },
  ];

  const [wallState, setWallState] = useState(0);
  const [coatState, setCoatState] = useState(1);
  //const [coatState, setCoatState] = useState(1);

  const addWall = () => {
    if (wallState < maxWalls) {
      setWallState(wallState + 1);
    }
  };

  const subWall = () => {
    if (wallState > minWalls) {
      setWallState(wallState - 1);
    }
  };

  const addCoat = () => {
    if (coatState < maxCoats) {
      setCoatState(coatState + 1);
    }
  };

  const subCoat = () => {
    if (coatState > minCoats) {
      setCoatState(coatState - 1);
    }
  };

  return (
    <main className="flex min-h-screen max-w-4xl flex-row justify-center mb-40 mt-16 mx-auto w-full">
      <div className="flex flex-col w-2/3 pr-5 border-r-2 border-gray-200">
        <div>
          <h2 className="mb-3 text-4xl font-semibold opacity-90">Settings</h2>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Walls</p>
            <div className="flex flex-row items-center  gap-3">
              <p className="font-bold text-3xl">{wallState}</p>
              <div className="flex flex-col text-2xl">
                <button onClick={addWall}>+</button>
                <button onClick={subWall}>-</button>
              </div>
            </div>
          </div>
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Coats</p>
            <div className="flex flex-row items-center  gap-3">
              <p className="font-bold text-3xl">{coatState}</p>
              <div className="flex flex-col text-2xl">
                <button onClick={addCoat}>+</button>
                <button onClick={subCoat}>-</button>
              </div>
            </div>
          </div>
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Brands</p>
            <Select
              size="sm"
              items={brands}
              label="Paint Brands"
              placeholder="Select a paint brand"
              className="max-w-xs"
            >
              {(brands) => (
                <SelectItem key={brands.value}>{brands.label}</SelectItem>
              )}
            </Select>
          </div>
        </div>
      </div>
      <div className="flex flex-col w-1/3">
        <div className="sticky top-5 pl-16">
          <div className="flex flex-col justify-between">
            <h2 className="mb-3 text-4xl font-semibold opacity-90">Total</h2>
          </div>
        </div>
      </div>
    </main>
  );
}
