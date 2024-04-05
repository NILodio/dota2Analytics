import {
  Container,
  Flex,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import useSWR from 'swr'
import { HEROES_API } from '../../constants/hero.const'
import { getHeroesAPI } from '../../utils/hero.api'

import { ItemsService } from "../../client"

import {HeroList} from "../../components/Dota/HeroList"
import {useFilteredHeroes} from "../../components/Dota/HeroFilter"
import {useHeroesByAttr} from "../../components/Dota/heroFilterAtt"

import useCustomToast from "../../hooks/useCustomToast"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const showToast = useCustomToast()
  const {test} = useSWR(HEROES_API, getHeroesAPI)
  const { filteredHeroes, heroFilter, setHeroFilter } = useFilteredHeroes(test)
  const { heroesByAttr, setHeroAttr } = useHeroesByAttr(test)
  const {
    data: items,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["items"],
    queryFn: () => ItemsService.readItems({}),
  })
  const heroes = heroFilter ? filteredHeroes : heroesByAttr

  console.log("isLoading:", isLoading);
  console.log("isError:", isError);
  console.log("heroes:", heroes);
  console.log("items:", items);
  console.log("test:", test);

  if (isError) {
    const errDetail = (error as any).body?.detail
    showToast("Something went wrong.", `${errDetail}`, "error")
  }

  return (
    <>
      {isLoading ? (
        // TODO: Add skeleton
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        heroes && (
          <Container maxW="full">
            <Heading
              size="lg"
              textAlign={{ base: "center", md: "left" }}
              pt={12}
            >
              Dota Winner
            </Heading>
            <HeroList heroes={heroes} />
          </Container>
        )
      )}
    </>
  )
}