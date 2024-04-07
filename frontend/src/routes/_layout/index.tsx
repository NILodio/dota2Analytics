import {
  Container,
  Flex,
  Heading,
  Spinner,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import {DotaService} from "../../client"
import {HeroList} from "../../components/Dota/HeroList"
import {useFilteredHeroes} from "../../components/Dota/HeroFilter"
import {useHeroesByAttr} from "../../components/Dota/HeroFilterAtt"

import { HeroFilterByAttribute } from "../../components/Dota/HeroFilterByAttribute"
import { HeroSearch } from "../../components/Dota/HeroSearch"
import { HeroNavbar } from "../../components/Dota/Navbar"

import useCustomToast from "../../hooks/useCustomToast"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const showToast = useCustomToast()
  const {
    data: heroes,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["heroes"],
    queryFn: () => DotaService.readHeroes({}),
  })

  const { filteredHeroes, heroFilter, setHeroFilter } = useFilteredHeroes(heroes?.data || [])
	const { heroesByAttr, setHeroAttr } = useHeroesByAttr(heroes?.data || [])
	const listHeroes = heroFilter ? filteredHeroes : heroesByAttr

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
            <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
              Dota Management
            </Heading>
            <Container maxW="full">
              <HeroNavbar>
                <HeroFilterByAttribute setHeroAttr={setHeroAttr} />
                <HeroSearch setHeroFilter={setHeroFilter} />
              </HeroNavbar>
              <HeroList heroes={listHeroes} />
            </Container>
          </Container>
        )
      )}
    </>
  )
}